import { defaultConfig } from '../../../src/config/config'
import { getRedisConnectionOptions } from '../../../src/utils/db/redis'

describe('Redis', () => {
    describe('getRedisConnectionOptions', () => {
        const config = { ...defaultConfig }

        beforeEach(() => {
            config.REDIS_URL = 'redis://localhost:6379'
            config.CLAIRVIEW_REDIS_HOST = 'clairview-redis'
            config.CLAIRVIEW_REDIS_PORT = 6379
            config.CLAIRVIEW_REDIS_PASSWORD = 'clairview-password'
            config.INGESTION_REDIS_HOST = 'ingestion-redis'
            config.INGESTION_REDIS_PORT = 6479
            config.CLAIRVIEW_SESSION_RECORDING_REDIS_HOST = 'session-recording-redis'
            config.CLAIRVIEW_SESSION_RECORDING_REDIS_PORT = 6579
        })

        it('should respond with unique options if all values set', () => {
            expect(getRedisConnectionOptions(config, 'clairview')).toMatchInlineSnapshot(`
                Object {
                  "options": Object {
                    "password": "clairview-password",
                    "port": 6379,
                  },
                  "url": "clairview-redis",
                }
            `)
            expect(getRedisConnectionOptions(config, 'ingestion')).toMatchInlineSnapshot(`
                Object {
                  "options": Object {
                    "port": 6479,
                  },
                  "url": "ingestion-redis",
                }
            `)
            expect(getRedisConnectionOptions(config, 'session-recording')).toMatchInlineSnapshot(`
                Object {
                  "options": Object {
                    "port": 6579,
                  },
                  "url": "session-recording-redis",
                }
            `)
        })

        it('should respond with REDIS_HOST if no options set', () => {
            config.CLAIRVIEW_REDIS_HOST = ''
            config.INGESTION_REDIS_HOST = ''
            config.CLAIRVIEW_SESSION_RECORDING_REDIS_HOST = ''

            expect(getRedisConnectionOptions(config, 'clairview')).toMatchInlineSnapshot(`
                Object {
                  "url": "redis://localhost:6379",
                }
            `)
            expect(getRedisConnectionOptions(config, 'ingestion')).toMatchInlineSnapshot(`
                Object {
                  "url": "redis://localhost:6379",
                }
            `)
            expect(getRedisConnectionOptions(config, 'session-recording')).toMatchInlineSnapshot(`
                Object {
                  "url": "redis://localhost:6379",
                }
            `)
        })

        it('should use the CLAIRVIEW_REDIS_HOST for ingestion if INGESTION_REDIS_HOST is not set', () => {
            config.INGESTION_REDIS_HOST = ''

            expect(getRedisConnectionOptions(config, 'ingestion')).toMatchInlineSnapshot(`
                Object {
                  "options": Object {
                    "password": "clairview-password",
                    "port": 6379,
                  },
                  "url": "clairview-redis",
                }
            `)
        })
    })
})
