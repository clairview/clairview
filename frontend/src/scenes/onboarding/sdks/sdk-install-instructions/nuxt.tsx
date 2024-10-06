import { useValues } from 'kea'
import { CodeSnippet, Language } from 'lib/components/CodeSnippet'
import { FEATURE_FLAGS } from 'lib/constants'
import { Link } from 'lib/lemon-ui/Link'
import { featureFlagLogic } from 'lib/logic/featureFlagLogic'
import { apiHostOrigin } from 'lib/utils/apiHost'
import { teamLogic } from 'scenes/teamLogic'

import { JSInstallSnippet } from './js-web'

function NuxtEnvVarsSnippet(): JSX.Element {
    const { currentTeam } = useValues(teamLogic)

    return (
        <CodeSnippet language={Language.JavaScript}>
            {`export default defineNuxtConfig({
                runtimeConfig: {
                  public: {
                    markettorPublicKey: '${currentTeam?.api_token}',
                    markettorHost: '${apiHostOrigin()}'
                  }
                }
              })`}
        </CodeSnippet>
    )
}

function NuxtAppClientCodeSnippet(): JSX.Element {
    const { featureFlags } = useValues(featureFlagLogic)
    const isPersonProfilesDisabled = featureFlags[FEATURE_FLAGS.PERSONLESS_EVENTS_NOT_SUPPORTED]
    return (
        <CodeSnippet language={Language.JavaScript}>
            {`import { defineNuxtPlugin } from '#app'
import markettor from 'markettor-js'
export default defineNuxtPlugin(nuxtApp => {
  const runtimeConfig = useRuntimeConfig();
  const markettorClient = markettor.init(runtimeConfig.public.markettorPublicKey, {
    api_host: runtimeConfig.public.markettorHost,
    ${
        isPersonProfilesDisabled
            ? ``
            : `person_profiles: 'identified_only', // or 'always' to create profiles for anonymous users as well`
    }
    capture_pageview: false, // we add manual pageview capturing below
    loaded: (markettor) => {
      if (import.meta.env.MODE === 'development') markettor.debug();
    }
  })

  // Make sure that pageviews are captured with each route change
  const router = useRouter();
  router.afterEach((to) => {
    nextTick(() => {
      markettor.capture('$pageview', {
        current_url: to.fullPath
      });
    });
  });

  return {
    provide: {
      markettor: () => markettorClient
    }
  }
})`}
        </CodeSnippet>
    )
}

export function SDKInstallNuxtJSInstructions(): JSX.Element {
    return (
        <>
            <p>
                The below guide is for Nuxt v3.0 and above. For Nuxt v2.16 and below, see our{' '}
                <Link to="https://markettor.com/docs/libraries/nuxt-js#nuxt-v216-and-below">Nuxt docs</Link>
            </p>
            <h3>Install markettor-js using your package manager</h3>
            <JSInstallSnippet />
            <h3>Add environment variables</h3>
            <p>
                Add your MarketTor API key and host to your <code>nuxt.config.js</code> file.
            </p>
            <NuxtEnvVarsSnippet />

            <h3>Create a plugin</h3>
            <p>
                Create a new plugin by creating a new file <code>markettor.client.js</code> in your{' '}
                <Link to="https://nuxt.com/docs/guide/directory-structure/plugins" target="_blank">
                    plugins directory
                </Link>
                :
            </p>
            <NuxtAppClientCodeSnippet />
        </>
    )
}
