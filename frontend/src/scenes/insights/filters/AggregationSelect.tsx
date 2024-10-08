import { LemonSelect, LemonSelectSection } from '@clairview/lemon-ui'
import { useActions, useValues } from 'kea'
import { TorQLEditor } from 'lib/components/TorQLEditor/TorQLEditor'
import { groupsAccessLogic } from 'lib/introductions/groupsAccessLogic'
import { GroupIntroductionFooter } from 'scenes/groups/GroupsIntroduction'
import { insightVizDataLogic } from 'scenes/insights/insightVizDataLogic'

import { groupsModel } from '~/models/groupsModel'
import { FunnelsQuery } from '~/queries/schema'
import { isFunnelsQuery, isInsightQueryNode, isStickinessQuery } from '~/queries/utils'
import { InsightLogicProps } from '~/types'

function getTorQLValue(groupIndex?: number, aggregationQuery?: string): string {
    if (groupIndex !== undefined) {
        return `$group_${groupIndex}`
    } else if (aggregationQuery) {
        return aggregationQuery
    }
    return UNIQUE_USERS
}

function torQLToFilterValue(value?: string): { groupIndex?: number; aggregationQuery?: string } {
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
    torqlAvailable?: boolean
    value?: string
}

export function AggregationSelect({
    insightProps,
    className,
    torqlAvailable,
}: AggregationSelectProps): JSX.Element | null {
    const { querySource } = useValues(insightVizDataLogic(insightProps))
    const { updateQuerySource } = useActions(insightVizDataLogic(insightProps))

    const { groupTypes, aggregationLabel } = useValues(groupsModel)
    const { needsUpgradeForGroups, canStartUsingGroups } = useValues(groupsAccessLogic)

    if (!isInsightQueryNode(querySource)) {
        return null
    }

    const value = getTorQLValue(
        isStickinessQuery(querySource) ? undefined : querySource.aggregation_group_type_index,
        isFunnelsQuery(querySource) ? querySource.funnelsFilter?.funnelAggregateByTorQL : undefined
    )
    const onChange = (value: string): void => {
        const { aggregationQuery, groupIndex } = torQLToFilterValue(value)
        if (isFunnelsQuery(querySource)) {
            updateQuerySource({
                aggregation_group_type_index: groupIndex,
                funnelsFilter: { ...querySource.funnelsFilter, funnelAggregateByTorQL: aggregationQuery },
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

    if (torqlAvailable) {
        baseValues.push(`properties.$session_id`)
        optionSections[0].options.push({
            value: 'properties.$session_id',
            label: `Unique sessions`,
        })
        optionSections[0].options.push({
            label: 'Custom TorQL expression',
            options: [
                {
                    // This is a bit of a hack so that the TorQL option is only highlighted as active when the user has
                    // set a custom value (because actually _all_ the options are TorQL)
                    value: !value || baseValues.includes(value) ? '' : value,
                    label: <span className="font-mono">{value}</span>,
                    labelInMenu: function CustomTorQLOptionWrapped({ onSelect }) {
                        return (
                            // eslint-disable-next-line react/forbid-dom-props
                            <div className="w-120" style={{ maxWidth: 'max(60vw, 20rem)' }}>
                                <TorQLEditor
                                    onChange={onSelect}
                                    value={value}
                                    placeholder={
                                        "Enter TorQL expression, such as:\n- distinct_id\n- properties.$session_id\n- concat(distinct_id, ' ', properties.$session_id)\n- if(1 < 2, 'one', 'two')"
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
