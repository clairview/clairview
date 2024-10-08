export const MMDB_ENDPOINT = 'https://mmdbcdn.clairview.net/'
export const MMDB_ATTACHMENT_KEY = '@clairview/mmdb'
export const MMDB_STALE_AGE_DAYS = 45
export const MMDB_STATUS_REDIS_KEY = '@clairview-plugin-server/mmdb-status'
export const MMDB_INTERNAL_SERVER_TIMEOUT_SECONDS = 10

export enum MMDBRequestStatus {
    TimedOut = 'Internal MMDB server connection timed out!',
    ServiceUnavailable = 'IP location capabilities are not available in this ClairView instance!',
    OK = 'OK',
}
