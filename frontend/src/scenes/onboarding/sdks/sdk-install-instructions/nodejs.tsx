import { useValues } from 'kea'
import { CodeSnippet, Language } from 'lib/components/CodeSnippet'
import { apiHostOrigin } from 'lib/utils/apiHost'
import { teamLogic } from 'scenes/teamLogic'

export function NodeInstallSnippet(): JSX.Element {
    return (
        <CodeSnippet language={Language.Bash}>
            {`npm install clairview-node
# OR
yarn add clairview-node
# OR
pnpm add clairview-node`}
        </CodeSnippet>
    )
}

export function NodeSetupSnippet(): JSX.Element {
    const { currentTeam } = useValues(teamLogic)

    return (
        <CodeSnippet language={Language.JavaScript}>
            {`import { ClairView } from 'clairview-node'

const client = new ClairView(
    '${currentTeam?.api_token}',
    { host: '${apiHostOrigin()}' }
)`}
        </CodeSnippet>
    )
}

export function SDKInstallNodeInstructions(): JSX.Element {
    return (
        <>
            <h3>Install</h3>
            <NodeInstallSnippet />
            <h3>Configure</h3>
            <NodeSetupSnippet />
        </>
    )
}
