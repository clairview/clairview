import { LemonSelect, LemonSelectSection } from '@clairview/lemon-ui'
import { useActions, useValues } from 'kea'
import { ClairQLEditor } from 'lib/components/ClairQLEditor/ClairQLEditor'
import { groupsAccessLogic } from 'lib/introductions/groupsAccessLogic'
import { GroupIntroductionFooter } from 'scenes/groups/GroupsIntroduction'
import { insightVizDataLogic } from 'scenes/insights/insightVizDataLogic'

import { groupsModel } from '~/models/groupsModel'
import { FunnelsQuery } from '~/queries/schema'
import { isFunnelsQuery, isInsightQueryNode, isStickinessQuery } from '~/queries/utils'
import { InsightLogicProps } from '~/types'

function getClairQLValue(groupIndex?: number, aggregationQuery?: string): string {
    if (groupIndex !== undefined) {
        return `$group_${groupIndex}`
    } else if (aggregationQuery) {
        return aggregationQuery
    }
    return UNIQUE_USERS
}

function clairQLToFilterValue(value?: string): { groupIndex?: number; aggregationQuery?: string } {
    if (value?.match(/^\$group_[0-9]+$/)) {
        return { groupIndex: parseInt(value.replace('$group_', '')) }
    } else if (value === 'person_id') {
        return {}
    }
    return { aggregationQuery: value }
}

const UNIQUE_USERS = 'person_id'

type AggregationSelectProps = {
    insightProps: InsightLogicProps
    className?: string
    clairqlAvailable?: boolean
    value?: string
}

export function AggregationSelect({
    insightProps,
    className,
    clairqlAvailable,
}: AggregationSelectProps): JSX.Element | null {
    const { querySource } = useValues(insightVizDataLogic(insightProps))
    const { updateQuerySource } = useActions(insightVizDataLogic(insightProps))

    const { groupTypes, aggregationLabel } = useValues(groupsModel)
    const { needsUpgradeForGroups, canStartUsingGroups } = useValues(groupsAccessLogic)

    if (!isInsightQueryNode(querySource)) {
        return null
    }

    const value = getClairQLValue(
        isStickinessQuery(querySource) ? undefined : querySource.aggregation_group_type_index,
        isFunnelsQuery(querySource) ? querySource.funnelsFilter?.funnelAggregateByClairQL : undefined
    )
    const onChange = (value: string): void => {
        const { aggregationQuery, groupIndex } = clairQLToFilterValue(value)
        if (isFunnelsQuery(querySource)) {
            updateQuerySource({
                aggregation_group_type_index: groupIndex,
                funnelsFilter: { ...querySource.funnelsFilter, funnelAggregateByClairQL: aggregationQuery },
            } as FunnelsQuery)
        } else {
            updateQuerySource({ aggregation_group_type_index: groupIndex } as FunnelsQuery)
        }
    }

    const baseValues = [UNIQUE_USERS]
    const optionSections: LemonSelectSection<string>[] = [
        {
            title: 'Event Aggregation',
            options: [
                {
                    value: UNIQUE_USERS,
                    label: 'Unique users',
                },
            ],
        },
    ]

    if (needsUpgradeForGroups || canStartUsingGroups) {
        optionSections[0].footer = <GroupIntroductionFooter needsUpgrade={needsUpgradeForGroups} />
    } else {
        Array.from(groupTypes.values()).forEach((groupType) => {
            baseValues.push(`$group_${groupType.group_type_index}`)
            optionSections[0].options.push({
                value: `$group_${groupType.group_type_index}`,
                label: `Unique ${aggregationLabel(groupType.group_type_index).plural}`,
            })
        })
    }

    if (clairqlAvailable) {
        baseValues.push(`properties.$session_id`)
        optionSections[0].options.push({
            value: 'properties.$session_id',
            label: `Unique sessions`,
        })
        optionSections[0].options.push({
            label: 'Custom ClairQL expression',
            options: [
                {
                    // This is a bit of a hack so that the ClairQL option is only highlighted as active when the user has
                    // set a custom value (because actually _all_ the options are ClairQL)
                    value: !value || baseValues.includes(value) ? '' : value,
                    label: <span className="font-mono">{value}</span>,
                    labelInMenu: function CustomClairQLOptionWrapped({ onSelect }) {
                        return (
                            // eslint-disable-next-line react/forbid-dom-props
                            <div className="w-120" style={{ maxWidth: 'max(60vw, 20rem)' }}>
                                <ClairQLEditor
                                    onChange={onSelect}
                                    value={value}
                                    placeholder={
                                        "Enter ClairQL expression, such as:\n- distinct_id\n- properties.$session_id\n- concat(distinct_id, ' ', properties.$session_id)\n- if(1 < 2, 'one', 'two')"
                                    }
                                />
                            </div>
                        )
                    },
                },
            ],
        })
    }

    return (
        <LemonSelect
            className={className || 'flex-1'}
            value={value}
            onChange={(newValue) => {
                if (newValue !== null) {
                    onChange(newValue)
                }
            }}
            data-attr="retention-aggregation-selector"
            dropdownMatchSelectWidth={false}
            options={optionSections}
        />
    )
}
