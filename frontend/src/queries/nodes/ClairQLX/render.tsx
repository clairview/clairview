import { LemonButton, Link } from '@clairview/lemon-ui'
import { useActions } from 'kea'
import { JSONViewer } from 'lib/components/JSONViewer'
import { Sparkline } from 'lib/components/Sparkline'
import { IconPlayCircle } from 'lib/lemon-ui/icons'
import { sessionPlayerModalLogic } from 'scenes/session-recordings/player/modal/sessionPlayerModalLogic'
import { urls } from 'scenes/urls'

import { ErrorBoundary } from '~/layout/ErrorBoundary'

export function parseClairQLX(value: any): any {
    if (!Array.isArray(value)) {
        return value
    }
    if (value[0] === '__hx_tag') {
        const object: Record<string, any> = {}
        const start = value[1] === '__hx_obj' ? 2 : 0
        for (let i = start; i < value.length; i += 2) {
            const key = parseClairQLX(value[i])
            object[key] = parseClairQLX(value[i + 1])
        }
        return object
    }
    return value.map((v) => parseClairQLX(v))
}

function ViewRecordingModalButton({ sessionId }: { sessionId: string }): JSX.Element {
    const { openSessionPlayer } = useActions(sessionPlayerModalLogic)
    return (
        <ErrorBoundary>
            <LemonButton
                type="primary"
                size="xsmall"
                sideIcon={<IconPlayCircle />}
                data-attr="clair-ql-view-recording-button"
                to={urls.replaySingle(sessionId)}
                onClick={(e) => {
                    e.preventDefault()
                    if (sessionId) {
                        openSessionPlayer({ id: sessionId })
                    }
                }}
                className="inline-block"
            >
                View recording
            </LemonButton>
        </ErrorBoundary>
    )
}

export function renderClairQLX(value: any): JSX.Element {
    const object = parseClairQLX(value)

    if (typeof object === 'object') {
        if (Array.isArray(object)) {
            return <JSONViewer src={object} name={null} collapsed={object.length > 10 ? 0 : 1} />
        }

        const { __hx_tag: tag, ...rest } = object
        if (!tag) {
            return <JSONViewer src={rest} name={null} collapsed={Object.keys(rest).length > 10 ? 0 : 1} />
        } else if (tag === 'Sparkline') {
            const { data, type, ...props } = rest
            return (
                <ErrorBoundary>
                    <Sparkline className="h-8" {...props} data={data ?? []} type={type} />
                </ErrorBoundary>
            )
        } else if (tag === 'RecordingButton') {
            const { sessionId, ...props } = rest
            return <ViewRecordingModalButton sessionId={sessionId} {...props} />
        } else if (tag === 'a') {
            const { href, source, target } = rest
            return (
                <ErrorBoundary>
                    <Link to={href} target={target ?? '_self'}>
                        {source ? renderClairQLX(source) : href}
                    </Link>
                </ErrorBoundary>
            )
        } else if (tag === 'strong') {
            const { source } = rest
            return (
                <ErrorBoundary>
                    <strong>{renderClairQLX(source)}</strong>
                </ErrorBoundary>
            )
        } else if (tag === 'em') {
            const { source } = rest
            return (
                <ErrorBoundary>
                    <em>{renderClairQLX(source)}</em>
                </ErrorBoundary>
            )
        }
        return <div>Unknown tag: {String(tag)}</div>
    }

    return <>{String(value)}</>
}