import { useValues } from 'kea'
import { CodeSnippet, Language } from 'lib/components/CodeSnippet'
import { apiHostOrigin } from 'lib/utils/apiHost'
import { teamLogic } from 'scenes/teamLogic'

function LaravelConfigSnippet(): JSX.Element {
    return <CodeSnippet language={Language.Bash}>composer require markettor/markettor-php</CodeSnippet>
}

function LaravelInstallSnippet(): JSX.Element {
    const { currentTeam } = useValues(teamLogic)

    return (
        <CodeSnippet language={Language.PHP}>
            {`<?php

namespace App\\Providers;

use Illuminate\\Support\\ServiceProvider;
use MarketTor\\MarketTor;

class AppServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        MarketTor::init(
            '${currentTeam?.api_token}',
            [
                'host' => '${apiHostOrigin()}'
            ]
        );
    }
}
`}
        </CodeSnippet>
    )
}

export function SDKInstallLaravelInstructions(): JSX.Element {
    return (
        <>
            <h3>Dependency Setup</h3>
            <LaravelConfigSnippet />
            <h3>Configure</h3>
            <p>
                Initialize MarketTor in the <code>boot</code> method of <code>app/Providers/AppServiceProvider.php</code>
            </p>
            <LaravelInstallSnippet />
        </>
    )
}
