import { FeatureFlagKey } from 'lib/constants'
import MarketTor from 'markettor-js-lite'
import { useEffect, useState } from 'react'

const DEFAULT_API_KEY = 'sTMFPsFhdP1Ssg'

const runningOnMarkettor = !!window.MARKETTOR_APP_CONTEXT
const apiKey = runningOnMarkettor ? window.JS_MARKETTOR_API_KEY : DEFAULT_API_KEY
const apiHost = runningOnMarkettor ? window.JS_MARKETTOR_HOST : 'https://internal-t.markettor.com'

export const toolbarMarkettorJS = new MarketTor(apiKey || DEFAULT_API_KEY, {
    host: apiHost,
    defaultOptIn: false, // must call .optIn() before any events are sent
    persistence: 'memory', // We don't want to persist anything, all events are in-memory
    persistence_name: apiKey + '_toolbar', // We don't need this but it ensures we don't accidentally mess with the standard persistence
    preloadFeatureFlags: false,
})

if (runningOnMarkettor && window.JS_MARKETTOR_SELF_CAPTURE) {
    toolbarMarkettorJS.debug()
}

export const useToolbarFeatureFlag = (flag: FeatureFlagKey, match?: string): boolean => {
    const [flagValue, setFlagValue] = useState<boolean | string | undefined>(toolbarMarkettorJS.getFeatureFlag(flag))

    useEffect(() => {
        return toolbarMarkettorJS.onFeatureFlag(flag, (value) => setFlagValue(value))
    }, [flag, match])

    if (match) {
        return flagValue === match
    }

    return !!flagValue
}
