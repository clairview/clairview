import { BatchExportService } from '~/types'

export const humanizeBatchExportName = (service: BatchExportService['type']): string => {
    switch (service) {
        case 'HTTP':
            return 'ClairView HTTP'
        default:
            return service
    }
}
