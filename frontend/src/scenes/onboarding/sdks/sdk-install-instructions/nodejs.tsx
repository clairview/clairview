import { useValues } from 'kea'
import { CodeSnippet, Language } from 'lib/components/CodeSnippet'
import { apiHostOrigin } from 'lib/utils/apiHost'
import { teamLogic } from 'scenes/teamLogic'

export function NodeInstallSnippet(): JSX.Element {
    return (
        <CodeSnippet language={Language.Bash}>
            {`npm install markettor-node
# OR
yarn add markettor-node
# OR
pnpm add markettor-node`}
        </CodeSnippet>
    )
}

export function NodeSetupSnippet(): JSX.Element {
    const { currentTeam } = useValues(teamLogic)

    return (
        <CodeSnippet language={Language.JavaScript}>
            {`import { MarketTor } from 'markettor-node'

const client = new MarketTor(
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
