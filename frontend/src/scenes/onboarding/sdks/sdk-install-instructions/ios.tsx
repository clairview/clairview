import { LemonBanner, Link } from '@markettor/lemon-ui'
import { useValues } from 'kea'
import { CodeSnippet, Language } from 'lib/components/CodeSnippet'
import { apiHostOrigin } from 'lib/utils/apiHost'
import { teamLogic } from 'scenes/teamLogic'

export interface iOSSetupProps {
    includeReplay?: boolean
}

function IOSInstallCocoaPodsSnippet(): JSX.Element {
    return <CodeSnippet language={Language.Ruby}>{'pod "MarketTor", "~> 3.0.0"'}</CodeSnippet>
}

function IOSInstallSPMSnippet(): JSX.Element {
    return (
        <CodeSnippet language={Language.Swift}>
            {`dependencies: [
  .package(url: "https://github.com/MarketTor/markettor-ios.git", from: "3.0.0")
]`}
        </CodeSnippet>
    )
}

function IOSSetupSnippet({ includeReplay }: iOSSetupProps): JSX.Element {
    const { currentTeam } = useValues(teamLogic)

    return (
        <CodeSnippet language={Language.Swift}>
            {`import Foundation
import MarketTor
import UIKit

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(_: UIApplication, didFinishLaunchingWithOptions _: [UIApplication.LaunchOptionsKey: Any]? = nil) -> Bool {
        let MARKETTOR_API_KEY = "${currentTeam?.api_token}"
        let MARKETTOR_HOST = "${apiHostOrigin()}"

        let config = MarketTorConfig(apiKey: MARKETTOR_API_KEY, host: MARKETTOR_HOST)
        ${
            includeReplay
                ? `
        // check https://markettor.com/docs/session-replay/ios#installation
        // for more config and to learn about how we capture sessions on mobile
        // and what to expect
        config.sessionReplay = true
        // choose whether to mask images or text
        config.sessionReplayConfig.maskAllImages = false
        config.sessionReplayConfig.maskAllTextInputs = true
        // screenshot is disabled by default
        // The screenshot may contain sensitive information, use with caution
        config.sessionReplayConfig.screenshotMode = true`
                : ''
        }
        MarketTorSDK.shared.setup(config)

        return true
    }
}`}
        </CodeSnippet>
    )
}

export function SDKInstallIOSInstructions(props: iOSSetupProps): JSX.Element {
    return (
        <>
            {props.includeReplay ? (
                <LemonBanner type="info">
                    🚧 NOTE: <Link to="https://markettor.com/docs/session-replay/mobile">Mobile recording</Link> is
                    currently in beta. We are keen to gather as much feedback as possible so if you try this out please
                    let us know. You can send feedback via the{' '}
                    <Link to="https://us.markettor.com/#panel=support%3Afeedback%3Asession_replay%3Alow">
                        in-app support panel
                    </Link>{' '}
                    or one of our other <Link to="https://markettor.com/docs/support-options">support options</Link>.
                </LemonBanner>
            ) : null}
            <h3>Install via CocoaPods</h3>
            <IOSInstallCocoaPodsSnippet />
            <h3>Or Install via SPM</h3>
            <IOSInstallSPMSnippet />
            <h3>Configure</h3>
            <IOSSetupSnippet {...props} />
        </>
    )
}

export function SDKInstallIOSTrackScreenInstructions(): JSX.Element {
    return (
        <>
            <p>
                With <code>configuration.captureScreenViews</code> set as <code>true</code>, MarketTor will try to record
                all screen changes automatically.
            </p>
            <p>
                If you want to manually send a new screen capture event, use the <code>screen</code> function.
            </p>
            <CodeSnippet
                language={Language.Swift}
            >{`MarketTorSDK.shared.screen("Dashboard", properties: ["fromIcon": "bottom"])`}</CodeSnippet>
        </>
    )
}
