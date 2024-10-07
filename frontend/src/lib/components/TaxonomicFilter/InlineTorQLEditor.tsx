import { TorQLEditor } from 'lib/components/TorQLEditor/TorQLEditor'
import { TaxonomicFilterValue } from 'lib/components/TaxonomicFilter/types'

import { AnyDataNode } from '~/queries/schema'

export interface InlineTorQLEditorProps {
    value?: TaxonomicFilterValue
    onChange: (value: TaxonomicFilterValue, item?: any) => void
    metadataSource?: AnyDataNode
}

export function InlineTorQLEditor({ value, onChange, metadataSource }: InlineTorQLEditorProps): JSX.Element {
    return (
        <>
            <div className="taxonomic-group-title">TorQL expression</div>
            <div className="px-2 pt-2">
                <TorQLEditor
                    onChange={onChange}
                    value={String(value ?? '')}
                    metadataSource={metadataSource}
                    submitText={value ? 'Update TorQL expression' : 'Add TorQL expression'}
                    disableAutoFocus // :TRICKY: No autofocus here. It's controlled in the TaxonomicFilter.
                />
            </div>
        </>
    )
}
