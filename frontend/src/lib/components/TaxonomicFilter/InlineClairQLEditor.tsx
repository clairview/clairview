import { ClairQLEditor } from 'lib/components/ClairQLEditor/ClairQLEditor'
import { TaxonomicFilterValue } from 'lib/components/TaxonomicFilter/types'

import { AnyDataNode } from '~/queries/schema'

export interface InlineClairQLEditorProps {
    value?: TaxonomicFilterValue
    onChange: (value: TaxonomicFilterValue, item?: any) => void
    metadataSource?: AnyDataNode
}

export function InlineClairQLEditor({ value, onChange, metadataSource }: InlineClairQLEditorProps): JSX.Element {
    return (
        <>
            <div className="taxonomic-group-title">ClairQL expression</div>
            <div className="px-2 pt-2">
                <ClairQLEditor
                    onChange={onChange}
                    value={String(value ?? '')}
                    metadataSource={metadataSource}
                    submitText={value ? 'Update ClairQL expression' : 'Add ClairQL expression'}
                    disableAutoFocus // :TRICKY: No autofocus here. It's controlled in the TaxonomicFilter.
                />
            </div>
        </>
    )
}
