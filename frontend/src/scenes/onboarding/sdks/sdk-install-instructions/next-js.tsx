import { useValues } from 'kea'
import { CodeSnippet, Language } from 'lib/components/CodeSnippet'
import { FEATURE_FLAGS } from 'lib/constants'
import { Link } from 'lib/lemon-ui/Link'
import { featureFlagLogic } from 'lib/logic/featureFlagLogic'
import { apiHostOrigin } from 'lib/utils/apiHost'
import { teamLogic } from 'scenes/teamLogic'

import { JSInstallSnippet } from './js-web'

function NextEnvVarsSnippet(): JSX.Element {
    const { currentTeam } = useValues(teamLogic)

    return (
        <CodeSnippet language={Language.Bash}>
            {[`NEXT_PUBLIC_MARKETTOR_KEY=${currentTeam?.api_token}`, `NEXT_PUBLIC_MARKETTOR_HOST=${apiHostOrigin()}`].join(
                '\n'
            )}
        </CodeSnippet>
    )
}

function NextPagesRouterCodeSnippet(): JSX.Element {
    const { featureFlags } = useValues(featureFlagLogic)
    const isPersonProfilesDisabled = featureFlags[FEATURE_FLAGS.PERSONLESS_EVENTS_NOT_SUPPORTED]
    return (
        <CodeSnippet language={Language.JavaScript}>
            {`// pages/_app.js
import clairview from "clairview-js"
import { ClairViewProvider } from 'clairview-js/react'

if (typeof window !== 'undefined') { // checks that we are client-side
  clairview.init(process.env.NEXT_PUBLIC_MARKETTOR_KEY, {
    api_host: process.env.NEXT_PUBLIC_MARKETTOR_HOST || '${apiHostOrigin()}',
    ${
        isPersonProfilesDisabled
            ? ``
            : `person_profiles: 'identified_only', // or 'always' to create profiles for anonymous users as well`
    }
    loaded: (clairview) => {
      if (process.env.NODE_ENV === 'development') clairview.debug() // debug mode in development
    },
  })
}

export default function App(
    { Component, pageProps: { session, ...pageProps } }
) {
    return (
        <>
            <ClairViewProvider client={clairview}>
                <Component {...pageProps} />
            </ClairViewProvider>
        </>
    )
}`}
        </CodeSnippet>
    )
}

function NextAppRouterCodeSnippet(): JSX.Element {
    const { featureFlags } = useValues(featureFlagLogic)
    const isPersonProfilesDisabled = featureFlags[FEATURE_FLAGS.PERSONLESS_EVENTS_NOT_SUPPORTED]
    return (
        <CodeSnippet language={Language.JavaScript}>
            {`// app/providers.js
'use client'
import clairview from 'clairview-js'
import { ClairViewProvider } from 'clairview-js/react'

if (typeof window !== 'undefined') {
  clairview.init(process.env.NEXT_PUBLIC_MARKETTOR_KEY, {
    api_host: process.env.NEXT_PUBLIC_MARKETTOR_HOST,
    ${
        isPersonProfilesDisabled
            ? ``
            : `person_profiles: 'identified_only', // or 'always' to create profiles for anonymous users as well`
    }
  })
}
export function CSClairViewProvider({ children }) {
    return <ClairViewProvider client={clairview}>{children}</ClairViewProvider>
}`}
        </CodeSnippet>
    )
}

function NextAppRouterLayoutSnippet(): JSX.Element {
    return (
        <CodeSnippet language={Language.JavaScript}>
            {`// app/layout.js
import './globals.css'
import { CSClairViewProvider } from './providers'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <CSClairViewProvider>
        <body>{children}</body>
      </CSClairViewProvider>
    </html>
  )
}`}
        </CodeSnippet>
    )
}

export function SDKInstallNextJSInstructions(): JSX.Element {
    return (
        <>
            <h3>Install clairview-js using your package manager</h3>
            <JSInstallSnippet />
            <h3>Add environment variables</h3>
            <p>
                Add your environment variables to your .env.local file and to your hosting provider (e.g. Vercel,
                Netlify, AWS). You can find your project API key in your project settings.
            </p>
            <p className="italic">
                These values need to start with <code className="not-italic">NEXT_PUBLIC_</code> to be accessible on the
                client-side.
            </p>
            <NextEnvVarsSnippet />

            <h3>Initialize</h3>
            <h4>With App router</h4>
            <p>
                If your Next.js app to uses the <Link to="https://nextjs.org/docs/app">app router</Link>, you can
                integrate ClairView by creating a providers file in your app folder. This is because the clairview-js
                library needs to be initialized on the client-side using the Next.js{' '}
                <Link to="https://nextjs.org/docs/getting-started/react-essentials#client-components" target="_blank">
                    <code>'use client'</code> directive
                </Link>
                .
            </p>
            <NextAppRouterCodeSnippet />
            <p>
                Afterwards, import the <code>PHProvider</code> component in your <code>app/layout.js</code> file and
                wrap your app with it.
            </p>
            <NextAppRouterLayoutSnippet />
            <h4>With Pages router</h4>
            <p>
                If your Next.js app uses the <Link to="https://nextjs.org/docs/pages">pages router</Link>, you can
                integrate ClairView at the root of your app (pages/_app.js).
            </p>
            <NextPagesRouterCodeSnippet />
        </>
    )
}
