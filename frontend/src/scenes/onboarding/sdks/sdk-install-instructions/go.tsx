import { useValues } from 'kea'
import { CodeSnippet, Language } from 'lib/components/CodeSnippet'
import { apiHostOrigin } from 'lib/utils/apiHost'
import { teamLogic } from 'scenes/teamLogic'

function GoInstallSnippet(): JSX.Element {
    return <CodeSnippet language={Language.Bash}>go get "github.com/ClairView/clairview-go"</CodeSnippet>
}

function GoSetupSnippet(): JSX.Element {
    const { currentTeam } = useValues(teamLogic)

    return (
        <CodeSnippet language={Language.Go}>
            {`package main
import (
    "github.com/ClairView/clairview-go"
)
func main() {
    client, _ := clairview.NewWithConfig("${currentTeam?.api_token}", clairview.Config{Endpoint: "${apiHostOrigin()}"})
    defer client.Close()
}`}
        </CodeSnippet>
    )
}

export function SDKInstallGoInstructions(): JSX.Element {
    return (
        <>
            <h3>Install</h3>
            <GoInstallSnippet />
            <h3>Configure</h3>
            <GoSetupSnippet />
        </>
    )
}
