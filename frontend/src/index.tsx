import '~/styles'

import { getContext } from 'kea'
import clairview from 'clairview-js'
import { ClairViewProvider } from 'clairview-js/react'
import { createRoot } from 'react-dom/client'
import { App } from 'scenes/App'

import { initKea } from './initKea'
import { ErrorBoundary } from './layout/ErrorBoundary'
import { loadClairViewJS } from './loadClairViewJS'

loadClairViewJS()
initKea()

// Expose `window.getReduxState()` to make snapshots to storybook easy
if (typeof window !== 'undefined') {
    // Disabled in production to prevent leaking secret data, personal API keys, etc
    if (process.env.NODE_ENV === 'development') {
        ;(window as any).getReduxState = () => getContext().store.getState()
    } else {
        ;(window as any).getReduxState = () => 'Disabled outside development!'
    }
}

function renderApp(): void {
    const root = document.getElementById('root')
    if (root) {
        createRoot(root).render(
            <ErrorBoundary>
                <ClairViewProvider client={clairview}>
                    <App />
                </ClairViewProvider>
            </ErrorBoundary>
        )
    } else {
        console.error('Attempted, but could not render ClairView app because <div id="root" /> is not found.')
    }
}

// Render react only when DOM has loaded - javascript might be cached and loaded before the page is ready.
if (document.readyState !== 'loading') {
    renderApp()
} else {
    document.addEventListener('DOMContentLoaded', renderApp)
}
