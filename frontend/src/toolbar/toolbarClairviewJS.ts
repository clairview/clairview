import { FeatureFlagKey } from 'lib/constants'
import ClairView from 'clairview-js-lite'
import { useEffect, useState } from 'react'

const DEFAULT_API_KEY = 'sTMFPsFhdP1Ssg'

const runningOnClairview = !!window.CLAIRVIEW_APP_CONTEXT
const apiKey = runningOnClairview ? window.JS_CLAIRVIEW_API_KEY : DEFAULT_API_KEY
const apiHost = runningOnClairview ? window.JS_CLAIRVIEW_HOST : 'https://internal-t.clairview.com'

export const toolbarClairviewJS = new ClairView(apiKey || DEFAULT_API_KEY, {
    host: apiHost,
    defaultOptIn: false, // must call .optIn() before any events are sent
    persistence: 'memory', // We don't want to persist anything, all events are in-memory
    persistence_name: apiKey + '_toolbar', // We don't need this but it ensures we don't accidentally mess with the standard persistence
    preloadFeatureFlags: false,
})

if (runningOnClairview && window.JS_CLAIRVIEW_SELF_CAPTURE) {
    toolbarClairviewJS.debug()
}

export const useToolbarFeatureFlag = (flag: FeatureFlagKey, match?: string): boolean => {
    const [flagValue, setFlagValue] = useState<boolean | string | undefined>(toolbarClairviewJS.getFeatureFlag(flag))

    useEffect(() => {
        return toolbarClairviewJS.onFeatureFlag(flag, (value) => setFlagValue(value))
    }, [flag, match])

    if (match) {
        return flagValue === match
    }

    return !!flagValue
}