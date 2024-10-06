import { MarketTor } from 'markettor-node'

import { Team } from '../types'

export const markettor = new MarketTor('sTMFPsFhdP1Ssg', {
    host: 'https://us.i.markettor.com',
})

if (process.env.NODE_ENV === 'test') {
    markettor.disable()
}

export const captureTeamEvent = (team: Team, event: string, properties: Record<string, any> = {}): void => {
    markettor.capture({
        distinctId: team.uuid,
        event,
        properties: {
            team: team.uuid,
            ...properties,
        },
        groups: {
            project: team.uuid,
            organization: team.organization_id,
            instance: process.env.SITE_URL ?? 'unknown',
        },
    })
}
