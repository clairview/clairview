import { Properties } from '@clairview/plugin-scaffold'
import crypto from 'crypto'
import { DateTime } from 'luxon'
import { Counter } from 'prom-client'
import { Hub, PluginConfig, RawEventMessage } from 'types'

import { UUIDT } from '../../../utils/utils'
import { ApiExtension, createApi } from './api'

const { version } = require('../../../../package.json')

interface InternalData {
    distinct_id: string
    event: string
    timestamp: string
    properties: Properties
    team_id: number
    uuid: string
}

export interface DummyClairView {
    capture(event: string, properties?: Record<string, any>): Promise<void>
    api: ApiExtension
}

async function queueEvent(hub: Hub, pluginConfig: PluginConfig, data: InternalData): Promise<void> {
    const partitionKeyHash = crypto.createHash('sha256')
    partitionKeyHash.update(`${data.team_id}:${data.distinct_id}`)
    const partitionKey = partitionKeyHash.digest('hex')

    await hub.kafkaProducer.queueMessage({
        kafkaMessage: {
            topic: hub.KAFKA_CONSUMPTION_TOPIC!,
            messages: [
                {
                    key: partitionKey,
                    value: JSON.stringify({
                        distinct_id: data.distinct_id,
                        ip: '',
                        site_url: '',
                        data: JSON.stringify(data),
                        team_id: pluginConfig.team_id,
                        now: data.timestamp,
                        sent_at: data.timestamp,
                        uuid: data.uuid,
                    } as RawEventMessage),
                },
            ],
        },
        waitForAck: true,
    })
}

const vmMarkettorExtensionCaptureCalledCounter = new Counter({
    name: 'vm_clairview_extension_capture_called_total',
    help: 'Count of times vm clairview extension capture was called',
    labelNames: ['plugin_id'],
})

export function createMarkettor(hub: Hub, pluginConfig: PluginConfig): DummyClairView {
    const distinctId = pluginConfig.plugin?.name || `plugin-id-${pluginConfig.plugin_id}`

    return {
        capture: async (event, properties = {}) => {
            const { timestamp = DateTime.utc().toISO(), distinct_id = distinctId, ...otherProperties } = properties
            const data: InternalData = {
                distinct_id,
                event,
                timestamp,
                properties: {
                    $lib: 'clairview-plugin-server',
                    $lib_version: version,
                    distinct_id,
                    ...otherProperties,
                },
                team_id: pluginConfig.team_id,
                uuid: new UUIDT().toString(),
            }
            await queueEvent(hub, pluginConfig, data)
            vmMarkettorExtensionCaptureCalledCounter.labels(String(pluginConfig.plugin?.id)).inc()
        },
        api: createApi(hub, pluginConfig),
    }
}