import { LemonMenuItem, LemonSkeleton, LemonTableColumn, lemonToast } from '@markettor/lemon-ui'
import { useValues } from 'kea'
import api from 'lib/api'
import { LemonTableLink } from 'lib/lemon-ui/LemonTable/LemonTableLink'
import { Link } from 'lib/lemon-ui/Link'
import { Tooltip } from 'lib/lemon-ui/Tooltip'
import { deleteWithUndo } from 'lib/utils/deleteWithUndo'
import markettor from 'markettor-js'
import IconHTTP from 'public/hedgehog/running-hog.png'
import IconS3 from 'public/services/aws-s3.png'
import IconBigQuery from 'public/services/bigquery.png'
import IconPostgres from 'public/services/postgres.png'
import IconRedshift from 'public/services/redshift.png'
import IconSnowflake from 'public/services/snowflake.png'
import { urls } from 'scenes/urls'

import {
    BatchExportConfiguration,
    BatchExportRun,
    BatchExportService,
    LogEntryLevel,
    PipelineNodeTab,
    PipelineStage,
    PluginConfigTypeNew,
    PluginType,
} from '~/types'

import { pipelineAccessLogic } from './pipelineAccessLogic'
import { PluginImage, PluginImageSize } from './PipelinePluginImage'
import {
    Destination,
    ImportApp,
    PipelineBackend,
    PluginBasedNode,
    SiteApp,
    Transformation,
    WebhookDestination,
} from './types'

const PLUGINS_ALLOWED_WITHOUT_DATA_PIPELINES_ARR = [
    // frontend apps
    'https://github.com/MarketTor/bug-report-app',
    'https://github.com/MarketTor/early-access-features-app',
    'https://github.com/MarketTor/notification-bar-app',
    'https://github.com/MarketTor/pineapple-mode-app',
    // filtering apps
    'https://github.com/MarketTor/downsampling-plugin',
    'https://github.com/MarketTor/markettor-filter-out-plugin',
    // transformation apps
    'https://github.com/MarketTor/language-url-splitter-app',
    'https://github.com/MarketTor/markettor-app-url-parameters-to-event-properties',
    'https://github.com/MarketTor/markettor-plugin-geoip',
    'https://github.com/MarketTor/markettor-url-normalizer-plugin',
    'https://github.com/MarketTor/property-filter-plugin',
    'https://github.com/MarketTor/semver-flattener-plugin',
    'https://github.com/MarketTor/taxonomy-plugin',
    'https://github.com/MarketTor/timestamp-parser-plugin',
    'https://github.com/MarketTor/user-agent-plugin',
]
export const PLUGINS_ALLOWED_WITHOUT_DATA_PIPELINES = new Set([...PLUGINS_ALLOWED_WITHOUT_DATA_PIPELINES_ARR])

const GLOBAL_EXPORT_PLUGINS = [
    // export apps
    'https://github.com/MarketTor/customerio-plugin',
    'https://github.com/MarketTor/hubspot-plugin',
    'https://github.com/MarketTor/pace-markettor-integration',
    'https://github.com/MarketTor/markettor-avo-plugin',
    'https://github.com/MarketTor/markettor-engage-so-plugin',
    'https://github.com/MarketTor/markettor-intercom-plugin',
    'https://github.com/MarketTor/markettor-laudspeaker-app',
    'https://github.com/MarketTor/markettor-patterns-app',
    'https://github.com/MarketTor/markettor-twilio-plugin',
    'https://github.com/MarketTor/markettor-variance-plugin',
    'https://github.com/MarketTor/rudderstack-markettor-plugin',
    'https://github.com/MarketTor/salesforce-plugin',
    'https://github.com/MarketTor/sendgrid-plugin',
    'https://github.com/MarketTor/markettor-loops-plugin',
]
export const GLOBAL_PLUGINS = new Set([...PLUGINS_ALLOWED_WITHOUT_DATA_PIPELINES_ARR, ...GLOBAL_EXPORT_PLUGINS])

export function capturePluginEvent(event: string, plugin: PluginType, pluginConfig: PluginConfigTypeNew): void {
    markettor.capture(event, {
        plugin_id: plugin.id,
        plugin_name: plugin.name,
        plugin_config_id: pluginConfig.id,
    })
}
export function captureBatchExportEvent(event: string, batchExport: BatchExportConfiguration): void {
    markettor.capture(event, {
        batch_export_id: batchExport.id,
        batch_export_name: batchExport.name,
        batch_export_destination_type: batchExport.destination.type,
    })
}

const PAGINATION_DEFAULT_MAX_PAGES = 10
export async function loadPaginatedResults(
    url: string | null,
    maxIterations: number = PAGINATION_DEFAULT_MAX_PAGES
): Promise<any[]> {
    let results: any[] = []
    for (let i = 0; i <= maxIterations; ++i) {
        if (!url) {
            break
        }

        const { results: partialResults, next } = await api.get(url)
        results = results.concat(partialResults)
        url = next
    }
    return results
}

type RenderAppProps = {
    /** If the plugin is null, a skeleton will be rendered. */
    plugin: PluginType | null
    imageSize?: PluginImageSize
}

export function getBatchExportUrl(service: BatchExportService['type']): string {
    return `https://markettor.com/docs/cdp/batch-exports/${service.toLowerCase()}`
}

export function RenderApp({ plugin, imageSize = 'small' }: RenderAppProps): JSX.Element {
    if (!plugin) {
        return <LemonSkeleton className="w-15 h-15" />
    }

    return (
        <div className="flex items-center gap-4">
            <Tooltip
                title={
                    <>
                        {plugin.name}
                        <br />
                        {plugin.description}
                        <br />
                        {plugin.url ? 'Click to view app source code' : 'No source code available'}
                    </>
                }
            >
                {plugin.url && plugin.plugin_type !== 'inline' ? (
                    <Link to={plugin.url} target="_blank">
                        <PluginImage plugin={plugin} size={imageSize} />
                    </Link>
                ) : (
                    <span>
                        <PluginImage plugin={plugin} size={imageSize} />
                    </span>
                )}
            </Tooltip>
        </div>
    )
}

export function RenderBatchExportIcon({
    type,
    size = 'small',
}: {
    type: BatchExportService['type']
    size?: 'small' | 'medium'
}): JSX.Element {
    const icon = {
        BigQuery: IconBigQuery,
        Postgres: IconPostgres,
        Redshift: IconRedshift,
        S3: IconS3,
        Snowflake: IconSnowflake,
        HTTP: IconHTTP,
    }[type]

    const sizePx = size === 'small' ? 30 : 60

    return (
        <div className="flex items-center gap-4">
            <Tooltip
                title={
                    <>
                        {type}
                        <br />
                        Click to view docs
                    </>
                }
            >
                <Link to={getBatchExportUrl(type)}>
                    <img src={icon} alt={type} height={sizePx} width={sizePx} />
                </Link>
            </Tooltip>
        </div>
    )
}

export function LogLevelDisplay(level: LogEntryLevel): JSX.Element {
    let color: string | undefined
    switch (level) {
        case 'DEBUG':
            color = 'text-muted'
            break
        case 'LOG':
            color = 'text-text-3000'
            break
        case 'INFO':
            color = 'text-primary'
            break
        case 'WARNING':
        case 'WARN':
            color = 'text-warning'
            break
        case 'ERROR':
            color = 'text-danger'
            break
        default:
            break
    }
    return <span className={color}>{level}</span>
}

export function nameColumn<
    T extends { stage: PipelineStage; id: number; name: string; description?: string }
>(): LemonTableColumn<T, 'name'> {
    return {
        title: 'Name',
        sticky: true,
        render: function RenderName(_, pipelineNode) {
            return (
                <LemonTableLink
                    to={urls.pipelineNode(pipelineNode.stage, pipelineNode.id, PipelineNodeTab.Configuration)}
                    title={
                        <>
                            <Tooltip title="Click to update configuration, view metrics, and more">
                                <span>{pipelineNode.name}</span>
                            </Tooltip>
                        </>
                    }
                    description={pipelineNode.description}
                />
            )
        },
    }
}
export function appColumn<T extends { plugin: Transformation['plugin'] }>(): LemonTableColumn<T, 'plugin'> {
    return {
        title: 'App',
        width: 0,
        render: function RenderAppInfo(_, pipelineNode) {
            return <RenderApp plugin={pipelineNode.plugin} />
        },
    }
}

function pluginMenuItems(node: PluginBasedNode): LemonMenuItem[] {
    if (node.plugin?.url) {
        return [
            {
                label: 'View app source code',
                to: node.plugin.url,
                targetBlank: true,
            },
        ]
    }
    return []
}

export function pipelineNodeMenuCommonItems(node: Transformation | SiteApp | ImportApp | Destination): LemonMenuItem[] {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const { canConfigurePlugins } = useValues(pipelineAccessLogic)

    const items: LemonMenuItem[] = [
        {
            label: canConfigurePlugins ? 'Edit configuration' : 'View configuration',
            to: urls.pipelineNode(node.stage, node.id, PipelineNodeTab.Configuration),
        },
        {
            label: 'View metrics',
            to: urls.pipelineNode(node.stage, node.id, PipelineNodeTab.Metrics),
        },
        {
            label: 'View logs',
            to: urls.pipelineNode(node.stage, node.id, PipelineNodeTab.Logs),
        },
    ]
    if (node.backend === PipelineBackend.Plugin) {
        items.concat(pluginMenuItems(node))
    }
    return items
}

export async function loadPluginsFromUrl(url: string): Promise<Record<number, PluginType>> {
    const results: PluginType[] = await api.loadPaginatedResults<PluginType>(url)
    return Object.fromEntries(results.map((plugin) => [plugin.id, plugin]))
}

export function pipelinePluginBackedNodeMenuCommonItems(
    node: Transformation | SiteApp | ImportApp | WebhookDestination,
    toggleEnabled: any,
    loadPluginConfigs: any,
    inOverview?: boolean
): LemonMenuItem[] {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const { canConfigurePlugins } = useValues(pipelineAccessLogic)

    return [
        {
            label: node.enabled ? 'Disable app' : 'Enable app',
            onClick: () =>
                toggleEnabled({
                    enabled: !node.enabled,
                    id: node.id,
                }),
            disabledReason: canConfigurePlugins ? undefined : 'You do not have permission to toggle.',
        },
        ...pipelineNodeMenuCommonItems(node),
        ...(!inOverview
            ? [
                  {
                      label: 'Delete app',
                      status: 'danger' as const, // for typechecker happiness
                      onClick: () => {
                          void deleteWithUndo({
                              endpoint: `plugin_config`,
                              object: {
                                  id: node.id,
                                  name: node.name,
                              },
                              callback: loadPluginConfigs,
                          })
                      },
                      disabledReason: canConfigurePlugins ? undefined : 'You do not have permission to delete.',
                  },
              ]
            : []),
    ]
}

export function checkPermissions(stage: PipelineStage, togglingToEnabledOrNew: boolean): boolean {
    if (stage === PipelineStage.ImportApp && togglingToEnabledOrNew) {
        lemonToast.error('Import apps are deprecated and cannot be enabled.')
        return false
    }
    return true
}

export function isRunInProgress(run: BatchExportRun): boolean {
    return ['Running', 'Starting'].includes(run.status)
}
