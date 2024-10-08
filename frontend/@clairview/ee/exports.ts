import { ClairViewEE } from './types'

export default async (): Promise<ClairViewEE> => {
    try {
        // this has to import it...
        // eslint-disable-next-line import/no-restricted-paths
        return (await import('../../../ee/frontend/exports')).default()
    } catch (e) {
        return {
            enabled: false,
        }
    }
}
