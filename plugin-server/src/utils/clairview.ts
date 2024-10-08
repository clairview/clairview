import { ClairView } from 'clairview-node'

import { Team } from '../types'

export const clairview = new ClairView('sTMFPsFhdP1Ssg', {
    host: 'https://us.i.clairview.com',
})

if (process.env.NODE_ENV === 'test') {
    clairview.disable()
}

export const captureTeamEvent = (team: Team, event: string, properties: Record<string, any> = {}): void => {
    clairview.capture({
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
