import { LemonButton, LemonInput, LemonModal, Link } from '@clairview/lemon-ui'
import { useActions } from 'kea'
import { LemonField } from 'lib/lemon-ui/LemonField'
import { useState } from 'react'
import { organizationLogic } from 'scenes/organizationLogic'

export function CreateOrganizationModal({
    isVisible,
    onClose,
    inline = false,
}: {
    isVisible: boolean
    onClose?: () => void
    inline?: boolean
}): JSX.Element {
    const { createOrganization } = useActions(organizationLogic)
    const [name, setName] = useState<string>('')

    const closeModal: () => void = () => {
        if (onClose) {
            onClose()
            if (name) {
                setName('')
            }
        }
    }
    const handleSubmit = (): void => {
        createOrganization(name)
        closeModal()
    }

    return (
        <LemonModal
            width={480}
            title="Create an organization"
            description={
                <p>
                    Organizations gather people building together.
                    <br />
                    <Link to="https://clairview.com/docs/user-guides/organizations-and-projects" target="_blank">
                        Learn more in ClairView Docs.
                    </Link>
                </p>
            }
            footer={
                <>
                    {onClose && (
                        <LemonButton type="secondary" onClick={() => onClose()}>
                            Cancel
                        </LemonButton>
                    )}
                    <LemonButton
                        type="primary"
                        onClick={() => handleSubmit()}
                        disabledReason={!name ? 'Think of a name!' : null}
                        data-attr="create-organization-ok"
                    >
                        Create organization
                    </LemonButton>
                </>
            }
            onClose={closeModal}
            isOpen={isVisible}
            inline={inline}
        >
            <LemonField.Pure label="Organization name">
                <LemonInput
                    placeholder="Acme Inc."
                    maxLength={64}
                    autoFocus
                    value={name}
                    onChange={(value) => setName(value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            handleSubmit()
                        }
                    }}
                    data-attr="organization-name-input"
                />
            </LemonField.Pure>
        </LemonModal>
    )
}
