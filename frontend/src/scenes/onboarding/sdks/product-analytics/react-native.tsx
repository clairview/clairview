import { CodeSnippet, Language } from 'lib/components/CodeSnippet'

import { SDKKey } from '~/types'

import { SDKInstallRNInstructions } from '../sdk-install-instructions'
import { AdvertiseMobileReplay } from '../session-replay/SessionReplaySDKInstructions'

function RNCaptureSnippet(): JSX.Element {
    return (
        <CodeSnippet language={Language.JSX}>{`// With hooks
import { useClairView } from 'clairview-react-native'

const MyComponent = () => {
    const clairview = useClairView()

    useEffect(() => {
        clairview.capture("MyComponent loaded", { foo: "bar" })
    }, [])
}
`}</CodeSnippet>
    )
}

export function ProductAnalyticsRNInstructions(): JSX.Element {
    return (
        <>
            <SDKInstallRNInstructions />
            <h3 className="mt-4">Optional: Send a manual event</h3>
            <p>Our package will autocapture events for you, but you can manually define events, too!</p>
            <RNCaptureSnippet />
            <AdvertiseMobileReplay context="product-analytics-onboarding" sdkKey={SDKKey.REACT_NATIVE} />
        </>
    )
}
