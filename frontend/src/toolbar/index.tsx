import '~/styles'
import './styles.scss'

import type { MarketTor } from 'markettor-js'
import { createRoot } from 'react-dom/client'

import { initKea } from '~/initKea'
import { ToolbarApp } from '~/toolbar/ToolbarApp'
import { ToolbarParams } from '~/types'
;(window as any)['ph_load_toolbar'] = function (toolbarParams: ToolbarParams, markettor: MarketTor) {
    initKea()
    const container = document.createElement('div')
    const root = createRoot(container)

    document.body.appendChild(container)

    if (!markettor) {
        console.warn(
            '⚠️⚠️⚠️ Loaded toolbar via old version of markettor-js that does not support feature flags. Please upgrade! ⚠️⚠️⚠️'
        )
    }

    root.render(
        <ToolbarApp
            {...toolbarParams}
            actionId={parseInt(String(toolbarParams.actionId))}
            jsURL={toolbarParams.jsURL || toolbarParams.apiURL}
            markettor={markettor}
        />
    )
}
/** @deprecated, use "ph_load_toolbar" instead */
;(window as any)['ph_load_editor'] = (window as any)['ph_load_toolbar']
