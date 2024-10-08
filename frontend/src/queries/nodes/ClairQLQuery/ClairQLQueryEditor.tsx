import { Monaco } from '@monaco-editor/react'
import { IconMagicWand, IconPlus, IconX } from '@clairview/icons'
import { LemonInput, Link } from '@clairview/lemon-ui'
import clsx from 'clsx'
import { useActions, useValues } from 'kea'
import { router } from 'kea-router'
import { FlaggedFeature } from 'lib/components/FlaggedFeature'
import { FEATURE_FLAGS } from 'lib/constants'
import { LemonBanner } from 'lib/lemon-ui/LemonBanner'
import { LemonButton } from 'lib/lemon-ui/LemonButton'
import { CodeEditor } from 'lib/monaco/CodeEditor'
import {
    activemodelStateKey,
    codeEditorLogic,
    CodeEditorLogicProps,
    editorModelsStateKey,
} from 'lib/monaco/codeEditorLogic'
import type { editor as importedEditor, IDisposable, Uri } from 'monaco-editor'
import { useEffect, useRef, useState } from 'react'
import { dataWarehouseSceneLogic } from 'scenes/data-warehouse/settings/dataWarehouseSceneLogic'
import { urls } from 'scenes/urls'

import { ClairQLQuery } from '~/queries/schema'

import { clairQLQueryEditorLogic } from './clairQLQueryEditorLogic'

export interface ClairQLQueryEditorProps {
    query: ClairQLQuery
    setQuery?: (query: ClairQLQuery) => void
    onChange?: (query: string) => void
    embedded?: boolean
    editorFooter?: (hasErrors: boolean, errors: string | null, isValidView: boolean) => JSX.Element
}

let uniqueNode = 0

const EDITOR_HEIGHT = 222

export function ClairQLQueryEditor(props: ClairQLQueryEditorProps): JSX.Element {
    const editorRef = useRef<HTMLDivElement | null>(null)

    const [key, setKey] = useState(() =>
        router.values.location.pathname.includes(urls.dataWarehouse()) ? router.values.location.pathname : uniqueNode++
    )

    useEffect(() => {
        if (router.values.location.pathname.includes(urls.dataWarehouse())) {
            setKey(router.values.location.pathname)
        }
    }, [router.values.location.pathname])

    const [monacoAndEditor, setMonacoAndEditor] = useState(
        null as [Monaco, importedEditor.IStandaloneCodeEditor] | null
    )
    const [monaco, editor] = monacoAndEditor ?? []
    const clairQLQueryEditorLogicProps = {
        query: props.query,
        setQuery: props.setQuery,
        onChange: props.onChange,
        key,
        editor,
        monaco,
    }
    const logic = clairQLQueryEditorLogic(clairQLQueryEditorLogicProps)
    const { queryInput, prompt, aiAvailable, promptError, promptLoading, multitab } = useValues(logic)
    const { setQueryInput, saveQuery, setPrompt, draftFromPrompt, saveAsView, onUpdateView } = useActions(logic)

    const codeEditorKey = `clairQLQueryEditor/${key}`

    const codeEditorLogicProps: CodeEditorLogicProps = {
        key: codeEditorKey,
        sourceQuery: props.query,
        query: queryInput,
        language: 'clairQL',
        metadataFilters: props.query.filters,
        multitab,
    }
    const { hasErrors, error, isValidView, activeModelUri, allModels } = useValues(
        codeEditorLogic(codeEditorLogicProps)
    )

    const { createModel, setModel, deleteModel, setModels, addModel, updateState } = useActions(
        codeEditorLogic(codeEditorLogicProps)
    )

    const { editingView } = useValues(
        dataWarehouseSceneLogic({
            monaco,
            editor,
        })
    )
    // Using useRef, not useState, as we don't want to reload the component when this changes.
    const monacoDisposables = useRef([] as IDisposable[])
    useEffect(() => {
        return () => {
            monacoDisposables.current.forEach((d) => d?.dispose())
        }
    }, [])

    useEffect(() => {
        if (monaco && activeModelUri && multitab) {
            const _model = monaco.editor.getModel(activeModelUri)
            const val = _model?.getValue()
            if (val) {
                setQueryInput(val)
                saveQuery()
            }
        }
    }, [activeModelUri])

    return (
        <div className="flex items-start gap-2">
            <div
                data-attr="clairql-query-editor"
                className={clsx(
                    'flex flex-col rounded space-y-2 w-full overflow-hidden',
                    !props.embedded && 'p-2 border'
                )}
            >
                <FlaggedFeature flag={FEATURE_FLAGS.ARTIFICIAL_HOG}>
                    <div className="flex gap-2">
                        <LemonInput
                            className="grow"
                            prefix={<IconMagicWand />}
                            value={prompt}
                            onPressEnter={() => draftFromPrompt()}
                            onChange={(value) => setPrompt(value)}
                            placeholder={
                                aiAvailable
                                    ? 'What do you want to know? How would you like to tweak the query?'
                                    : 'To use AI features, set environment variable OPENAI_API_KEY for this instance of ClairView'
                            }
                            disabled={!aiAvailable}
                            maxLength={400}
                        />
                        <LemonButton
                            type="primary"
                            onClick={() => draftFromPrompt()}
                            disabledReason={
                                !aiAvailable
                                    ? 'Environment variable OPENAI_API_KEY is unset for this instance of ClairView'
                                    : !prompt
                                    ? 'Provide a prompt first'
                                    : null
                            }
                            tooltipPlacement="left"
                            loading={promptLoading}
                        >
                            Think
                        </LemonButton>
                    </div>
                </FlaggedFeature>
                {promptError ? <LemonBanner type="warning">{promptError}</LemonBanner> : null}
                <div className="relative flex-1 overflow-hidden flex-col">
                    {multitab && (
                        <div className="flex flex-row overflow-scroll hide-scrollbar">
                            {allModels.map((model) => (
                                <QueryTab
                                    key={model.path}
                                    active={model.path === activeModelUri?.path}
                                    model={model}
                                    onClick={setModel}
                                    onClear={allModels.length > 1 ? deleteModel : undefined}
                                />
                            ))}
                            <LemonButton
                                onClick={() => {
                                    createModel()
                                }}
                                icon={<IconPlus fontSize={14} />}
                            />
                        </div>
                    )}
                    {/* eslint-disable-next-line react/forbid-dom-props */}
                    <div ref={editorRef} className="resize-y overflow-hidden" style={{ height: EDITOR_HEIGHT }}>
                        <CodeEditor
                            queryKey={codeEditorKey}
                            sourceQuery={props.query}
                            className="border rounded-b overflow-hidden h-full"
                            language="clairQL"
                            value={queryInput}
                            onChange={(v) => {
                                setQueryInput(v ?? '')
                                updateState()
                            }}
                            height="100%"
                            onMount={(editor, monaco) => {
                                setMonacoAndEditor([monaco, editor])

                                const allModelQueries = localStorage.getItem(editorModelsStateKey(codeEditorKey))
                                const activeModelUri = localStorage.getItem(activemodelStateKey(codeEditorKey))

                                if (allModelQueries && multitab) {
                                    // clear existing models
                                    monaco.editor.getModels().forEach((model) => {
                                        model.dispose()
                                    })

                                    const models = JSON.parse(allModelQueries || '[]')
                                    const newModels: Uri[] = []

                                    models.forEach((model: Record<string, any>) => {
                                        if (monaco) {
                                            const uri = monaco.Uri.parse(model.path)
                                            const newModel = monaco.editor.createModel(model.query, 'clairQL', uri)
                                            editor?.setModel(newModel)
                                            newModels.push(uri)
                                        }
                                    })

                                    setModels(newModels)

                                    if (activeModelUri) {
                                        const uri = monaco.Uri.parse(activeModelUri)
                                        const activeModel = monaco.editor
                                            .getModels()
                                            .find((model) => model.uri.path === uri.path)
                                        activeModel && editor?.setModel(activeModel)
                                        const val = activeModel?.getValue()
                                        if (val) {
                                            setQueryInput(val)
                                            saveQuery()
                                        }
                                        setModel(uri)
                                    } else if (newModels.length) {
                                        setModel(newModels[0])
                                    }
                                } else {
                                    const model = editor.getModel()

                                    if (model) {
                                        addModel(model.uri)
                                        setModel(model.uri)
                                    }
                                }
                            }}
                            onPressCmdEnter={(value, selectionType) => {
                                if (value && selectionType === 'selection') {
                                    saveQuery(value)
                                } else {
                                    saveQuery()
                                }
                            }}
                            options={{
                                minimap: {
                                    enabled: false,
                                },
                                wordWrap: 'on',
                                scrollBeyondLastLine: false,
                                automaticLayout: true,
                                fixedOverflowWidgets: true,
                                suggest: {
                                    showInlineDetails: true,
                                },
                                quickSuggestionsDelay: 300,
                            }}
                        />
                    </div>
                </div>
                <div className="flex flex-row px-px">
                    {props.editorFooter ? (
                        props.editorFooter(hasErrors, error, isValidView)
                    ) : (
                        <>
                            <div className="flex-1">
                                <LemonButton
                                    onClick={() => saveQuery()}
                                    type="primary"
                                    disabledReason={
                                        !props.setQuery
                                            ? 'No permission to update'
                                            : hasErrors
                                            ? error ?? 'Query has errors'
                                            : undefined
                                    }
                                    center
                                    fullWidth
                                    data-attr="clairql-query-editor-save"
                                >
                                    {!props.setQuery ? 'No permission to update' : 'Update and run'}
                                </LemonButton>
                            </div>
                            {editingView ? (
                                <LemonButton
                                    className="ml-2"
                                    onClick={onUpdateView}
                                    type="primary"
                                    center
                                    disabledReason={
                                        hasErrors
                                            ? error ?? 'Query has errors'
                                            : !isValidView
                                            ? 'All fields must have an alias'
                                            : ''
                                    }
                                    data-attr="clairql-query-editor-update-view"
                                >
                                    Update view
                                </LemonButton>
                            ) : (
                                <LemonButton
                                    className="ml-2"
                                    onClick={saveAsView}
                                    type="primary"
                                    center
                                    disabledReason={
                                        hasErrors
                                            ? error ?? 'Query has errors'
                                            : !isValidView
                                            ? 'All fields must have an alias'
                                            : ''
                                    }
                                    data-attr="clairql-query-editor-save-as-view"
                                    tooltip={
                                        <div>
                                            Save a query as a view that can be referenced in another query. This is
                                            useful for modeling data and organizing large queries into readable chunks.{' '}
                                            <Link to="https://clairview.com/docs/data-warehouse">More Info</Link>{' '}
                                        </div>
                                    }
                                >
                                    Save as view
                                </LemonButton>
                            )}
                        </>
                    )}
                </div>
            </div>
        </div>
    )
}

// one off component for query editor tabs
interface QueryTabProps {
    model: Uri
    active?: boolean
    onClick?: (model: Uri) => void
    onClear?: (model: Uri) => void
}

function QueryTab({ model, active, onClear, onClick }: QueryTabProps): JSX.Element {
    return (
        <button
            onClick={() => onClick?.(model)}
            className={clsx(
                'space-y-px rounded-t p-1 flex flex-row items-center gap-1 hover:bg-[var(--bg-light)] cursor-pointer',
                active ? 'bg-[var(--bg-light)] border' : 'bg-bg-3000',
                onClear ? 'pl-3 pr-2' : 'px-4'
            )}
        >
            {'Query ' + model.path.split('/').pop()}
            {onClear && (
                <LemonButton
                    onClick={(e) => {
                        e.stopPropagation()
                        onClear(model)
                    }}
                    size="xsmall"
                    icon={<IconX />}
                />
            )}
        </button>
    )
}
