import { IconQueryEditor } from 'lib/lemon-ui/icons'
import { LemonButton, LemonButtonWithoutSideActionProps } from 'lib/lemon-ui/LemonButton'
import { urls } from 'scenes/urls'

import { DataTableNode, NodeKind } from '~/queries/schema'

export interface EditTorQLButtonProps extends LemonButtonWithoutSideActionProps {
    torql: string
}

export function EditTorQLButton({ torql, ...props }: EditTorQLButtonProps): JSX.Element {
    const query: DataTableNode = {
        kind: NodeKind.DataTableNode,
        full: true,
        source: { kind: NodeKind.TorQLQuery, query: torql },
    }
    return (
        <LemonButton
            data-attr="open-json-editor-button"
            type="secondary"
            to={urls.insightNew(undefined, undefined, query)}
            icon={<IconQueryEditor />}
            tooltip="Edit SQL directly"
            {...props}
        />
    )
}
