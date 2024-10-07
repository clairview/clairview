import { useActions, useValues } from 'kea'
import { TaxonomicFilterGroupType } from 'lib/components/TaxonomicFilter/types'
import { TaxonomicPopover } from 'lib/components/TaxonomicPopover/TaxonomicPopover'
import { pathsDataLogic } from 'scenes/paths/pathsDataLogic'

import { taxonomicEventFilterToTorQL } from '~/queries/utils'
import { EditorFilterProps } from '~/types'

export function PathsTorQL({ insightProps }: EditorFilterProps): JSX.Element {
    const { pathsFilter } = useValues(pathsDataLogic(insightProps))
    const { updateInsightFilter } = useActions(pathsDataLogic(insightProps))

    return (
        <TaxonomicPopover
            groupType={TaxonomicFilterGroupType.TorQLExpression}
            value={pathsFilter?.pathsTorQLExpression || 'event'}
            data-attr="paths-torql-expression"
            fullWidth
            onChange={(v, g) => {
                const torQl = taxonomicEventFilterToTorQL(g, v)
                if (torQl) {
                    updateInsightFilter({ pathsTorQLExpression: torQl })
                }
            }}
            groupTypes={[TaxonomicFilterGroupType.TorQLExpression]}
        />
    )
}
