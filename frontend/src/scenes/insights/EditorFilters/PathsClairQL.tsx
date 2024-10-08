import { useActions, useValues } from 'kea'
import { TaxonomicFilterGroupType } from 'lib/components/TaxonomicFilter/types'
import { TaxonomicPopover } from 'lib/components/TaxonomicPopover/TaxonomicPopover'
import { pathsDataLogic } from 'scenes/paths/pathsDataLogic'

import { taxonomicEventFilterToClairQL } from '~/queries/utils'
import { EditorFilterProps } from '~/types'

export function PathsClairQL({ insightProps }: EditorFilterProps): JSX.Element {
    const { pathsFilter } = useValues(pathsDataLogic(insightProps))
    const { updateInsightFilter } = useActions(pathsDataLogic(insightProps))

    return (
        <TaxonomicPopover
            groupType={TaxonomicFilterGroupType.ClairQLExpression}
            value={pathsFilter?.pathsClairQLExpression || 'event'}
            data-attr="paths-clairql-expression"
            fullWidth
            onChange={(v, g) => {
                const clairQl = taxonomicEventFilterToClairQL(g, v)
                if (clairQl) {
                    updateInsightFilter({ pathsClairQLExpression: clairQl })
                }
            }}
            groupTypes={[TaxonomicFilterGroupType.ClairQLExpression]}
        />
    )
}
