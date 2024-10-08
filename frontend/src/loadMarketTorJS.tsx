import * as Sentry from '@sentry/react'
import { FEATURE_FLAGS } from 'lib/constants'
import clairview, { ClairViewConfig } from 'clairview-js'

const configWithSentry = (config: Partial<ClairViewConfig>): Partial<ClairViewConfig> => {
    if ((window as any).SENTRY_DSN) {
        config.on_xhr_error = (failedRequest: XMLHttpRequest) => {
            const status = failedRequest.status
            const statusText = failedRequest.statusText || 'no status text in error'
            Sentry.captureException(
                new Error(`Failed with status ${status} while sending to ClairView. Message: ${statusText}`),
                { tags: { status, statusText } }
            )
        }
    }
    return config
}

export function loadClairViewJS(): void {
    if (window.JS_MARKETTOR_API_KEY) {
        clairview.init(
            window.JS_MARKETTOR_API_KEY,
            configWithSentry({
                opt_out_useragent_filter: window.location.hostname === 'localhost', // we ARE a bot when running in localhost, so we need to enable this opt-out
                api_host: window.JS_MARKETTOR_HOST,
                ui_host: window.JS_MARKETTOR_UI_HOST,
                rageclick: true,
                persistence: 'localStorage+cookie',
                bootstrap: window.MARKETTOR_USER_IDENTITY_WITH_FLAGS ? window.MARKETTOR_USER_IDENTITY_WITH_FLAGS : {},
                opt_in_site_apps: true,
                api_transport: 'fetch',
                loaded: (clairview) => {
                    if (clairview.sessionRecording) {
                        clairview.sessionRecording._forceAllowLocalhostNetworkCapture = true
                    }

                    if (window.IMPERSONATED_SESSION) {
                        clairview.opt_out_capturing()
                    } else {
                        clairview.opt_in_capturing()
                    }
                },
                scroll_root_selector: ['main', 'html'],
                autocapture: {
                    capture_copied_text: true,
                },
                person_profiles: 'always',

                // Helper to capture events for assertions in Cypress
                _onCapture: (window as any)._cypress_clairview_captures
                    ? (_, event) => (window as any)._cypress_clairview_captures.push(event)
                    : undefined,
            })
        )

        const Cypress = (window as any).Cypress

        if (Cypress) {
            Object.entries(Cypress.env()).forEach(([key, value]) => {
                if (key.startsWith('MARKETTOR_PROPERTY_')) {
                    clairview.register_for_session({
                        [key.replace('MARKETTOR_PROPERTY_', 'E2E_TESTING_').toLowerCase()]: value,
                    })
                }
            })
        }

        // This is a helpful flag to set to automatically reset the recording session on load for testing multiple recordings
        const shouldResetSessionOnLoad = clairview.getFeatureFlag(FEATURE_FLAGS.SESSION_RESET_ON_LOAD)
        if (shouldResetSessionOnLoad) {
            clairview.sessionManager?.resetSessionId()
        }
        // Make sure we have access to the object in window for debugging
        window.clairview = clairview
    } else {
        clairview.init('fake token', {
            autocapture: false,
            loaded: function (ph) {
                ph.opt_out_capturing()
            },
        })
    }

    if (window.SENTRY_DSN) {
        Sentry.init({
            dsn: window.SENTRY_DSN,
            environment: window.SENTRY_ENVIRONMENT,
            ...(location.host.includes('clairview.com') && {
                integrations: [new clairview.SentryIntegration(clairview, 'clairview', 1899813, undefined, '*')],
            }),
        })
    }
}
