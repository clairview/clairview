import { Link } from '@clairview/lemon-ui'
import { useValues } from 'kea'
import defaultLogo from 'public/clairview-logo.svg'
import cloudLogo from 'public/clairview-logo-cloud.svg'
import demoLogo from 'public/clairview-logo-demo.svg'
import { preflightLogic } from 'scenes/PreflightCheck/preflightLogic'

export function WelcomeLogo({ view }: { view?: string }): JSX.Element {
    const UTM_TAGS = `utm_campaign=in-product&utm_tag=${view || 'welcome'}-header`
    const { preflight } = useValues(preflightLogic)

    return (
        <Link to={`https://clairview.com?${UTM_TAGS}`} className="flex flex-col items-center mb-8">
            <img
                src={preflight?.demo ? demoLogo : preflight?.cloud ? cloudLogo : defaultLogo}
                alt={`ClairView${preflight?.cloud ? ' Cloud' : ''}`}
                className="h-6"
            />
        </Link>
    )
}
