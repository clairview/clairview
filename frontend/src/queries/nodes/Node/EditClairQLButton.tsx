import { IconQueryEditor } from 'lib/lemon-ui/icons'
import { LemonButton, LemonButtonWithoutSideActionProps } from 'lib/lemon-ui/LemonButton'
import { urls } from 'scenes/urls'

import { DataTableNode, NodeKind } from '~/queries/schema'

export interface EditClairQLButtonProps extends LemonButtonWithoutSideActionProps {
    clairql: string
}

export function EditClairQLButton({ clairql, ...props }: EditClairQLButtonProps): JSX.Element {
    const query: DataTableNode = {
        kind: NodeKind.DataTableNode,
        full: true,
        source: { kind: NodeKind.ClairQLQuery, query: clairql },
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
