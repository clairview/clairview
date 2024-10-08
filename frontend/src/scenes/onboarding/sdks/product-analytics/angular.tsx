import { LemonDivider } from '@clairview/lemon-ui'

import { SDKInstallAngularInstructions } from '../sdk-install-instructions/angular'
import { ProductAnalyticsAllJSFinalSteps } from './AllJSFinalSteps'

export function ProductAnalyticsAngularInstructions(): JSX.Element {
    return (
        <>
            <SDKInstallAngularInstructions />
            <LemonDivider thick dashed className="my-4" />
            <ProductAnalyticsAllJSFinalSteps />
        </>
    )
}
