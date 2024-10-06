import { MarketTorEE } from '@markettor/ee/types'

import { transformEventToWeb, transformToWeb } from './mobile-replay'

export default async (): Promise<MarketTorEE> =>
    Promise.resolve({
        enabled: true,
        mobileReplay: {
            transformEventToWeb,
            transformToWeb,
        },
    })
