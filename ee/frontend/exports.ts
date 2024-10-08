import { ClairViewEE } from '@clairview/ee/types'

import { transformEventToWeb, transformToWeb } from './mobile-replay'

export default async (): Promise<ClairViewEE> =>
    Promise.resolve({
        enabled: true,
        mobileReplay: {
            transformEventToWeb,
            transformToWeb,
        },
    })
