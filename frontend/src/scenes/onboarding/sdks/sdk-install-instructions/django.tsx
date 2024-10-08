import { useValues } from 'kea'
import { CodeSnippet, Language } from 'lib/components/CodeSnippet'
import { apiHostOrigin } from 'lib/utils/apiHost'
import { teamLogic } from 'scenes/teamLogic'

function DjangoInstallSnippet(): JSX.Element {
    return <CodeSnippet language={Language.Bash}>pip install clairview</CodeSnippet>
}

function DjangoAppConfigSnippet(): JSX.Element {
    const { currentTeam } = useValues(teamLogic)

    return (
        <CodeSnippet language={Language.Python}>
            {`from django.apps import AppConfig
import clairview

class YourAppConfig(AppConfig):
    name = "your_app_name"
    def ready(self):
        clairview.api_key = '${currentTeam?.api_token}'
        clairview.host = '${apiHostOrigin()}'`}
        </CodeSnippet>
    )
}

function DjangoSettingsSnippet(): JSX.Element {
    return (
        <CodeSnippet language={Language.Python}>
            {`INSTALLED_APPS = [
    # other apps
    'your_app_name.apps.MyAppConfig',  # Add your app config
] `}
        </CodeSnippet>
    )
}

export function SDKInstallDjangoInstructions(): JSX.Element {
    return (
        <>
            <h3>Install</h3>
            <DjangoInstallSnippet />
            <h3>Configure</h3>
            <p>
                Set the ClairView API key and host in your <code>AppConfig</code> in <code>apps.py</code> so that's it's
                available everywhere:
            </p>
            <DjangoAppConfigSnippet />
            <p />
            Next, if you haven't done so already, make sure you add your <code>AppConfig</code> to your{' '}
            <code>settings.py</code> under <code>INSTALLED_APPS</code>:
            <DjangoSettingsSnippet />
        </>
    )
}
