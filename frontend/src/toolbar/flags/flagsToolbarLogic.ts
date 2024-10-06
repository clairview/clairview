import Fuse from 'fuse.js'
import { actions, connect, kea, listeners, path, reducers, selectors } from 'kea'
import { loaders } from 'kea-loaders'
import { encodeParams } from 'kea-router'
import { permanentlyMount } from 'lib/utils/kea-logic-builders'
import type { MarketTor } from 'markettor-js'

import { toolbarConfigLogic, toolbarFetch } from '~/toolbar/toolbarConfigLogic'
import { toolbarMarkettorJS } from '~/toolbar/toolbarMarkettorJS'
import { CombinedFeatureFlagAndValueType } from '~/types'

import type { flagsToolbarLogicType } from './flagsToolbarLogicType'

export const flagsToolbarLogic = kea<flagsToolbarLogicType>([
    path(['toolbar', 'flags', 'flagsToolbarLogic']),
    connect(() => ({
        values: [toolbarConfigLogic, ['markettor']],
    })),
    actions({
        getUserFlags: true,
        setFeatureFlagValueFromMarketTorClient: (flags: string[], variants: Record<string, string | boolean>) => ({
            flags,
            variants,
        }),
        setOverriddenUserFlag: (flagKey: string, overrideValue: string | boolean) => ({ flagKey, overrideValue }),
        deleteOverriddenUserFlag: (flagKey: string) => ({ flagKey }),
        setSearchTerm: (searchTerm: string) => ({ searchTerm }),
        checkLocalOverrides: true,
        storeLocalOverrides: (localOverrides: Record<string, string | boolean>) => ({ localOverrides }),
    }),
    loaders(({ values }) => ({
        userFlags: [
            [] as CombinedFeatureFlagAndValueType[],
            {
                getUserFlags: async (_, breakpoint) => {
                    const params = {
                        groups: getGroups(values.markettor),
                    }
                    const response = await toolbarFetch(
                        `/api/projects/@current/feature_flags/my_flags${encodeParams(params, '?')}`
                    )

                    breakpoint()
                    if (!response.ok) {
                        return []
                    }
                    return await response.json()
                },
            },
        ],
    })),
    reducers({
        localOverrides: [
            {} as Record<string, string | boolean>,
            {
                storeLocalOverrides: (_, { localOverrides }) => localOverrides,
            },
        ],
        searchTerm: [
            '',
            {
                setSearchTerm: (_, { searchTerm }) => searchTerm,
            },
        ],
        markettorClientFlagValues: [
            {} as Record<string, string | boolean>,
            {
                setFeatureFlagValueFromMarketTorClient: (_, { variants }) => {
                    return variants
                },
            },
        ],
    }),
    selectors({
        userFlagsWithOverrideInfo: [
            (s) => [s.userFlags, s.localOverrides, s.markettorClientFlagValues],
            (userFlags, localOverrides, markettorClientFlagValues) => {
                return userFlags.map((flag) => {
                    const hasVariants = (flag.feature_flag.filters?.multivariate?.variants?.length || 0) > 0

                    const currentValue =
                        flag.feature_flag.key in localOverrides
                            ? localOverrides[flag.feature_flag.key]
                            : markettorClientFlagValues[flag.feature_flag.key] ?? flag.value

                    return {
                        ...flag,
                        hasVariants,
                        currentValue,
                        hasOverride: flag.feature_flag.key in localOverrides,
                    }
                })
            },
        ],
        filteredFlags: [
            (s) => [s.searchTerm, s.userFlagsWithOverrideInfo],
            (searchTerm, userFlagsWithOverrideInfo) => {
                return searchTerm
                    ? new Fuse(userFlagsWithOverrideInfo, {
                          threshold: 0.3,
                          keys: ['feature_flag.key', 'feature_flag.name'],
                      })
                          .search(searchTerm)
                          .map(({ item }) => item)
                    : userFlagsWithOverrideInfo
            },
        ],
        countFlagsOverridden: [(s) => [s.localOverrides], (localOverrides) => Object.keys(localOverrides).length],
    }),
    listeners(({ actions, values }) => ({
        checkLocalOverrides: () => {
            const clientMarketTor = values.markettor
            if (clientMarketTor) {
                const locallyOverrideFeatureFlags = clientMarketTor.get_property('$override_feature_flags') || {}
                actions.storeLocalOverrides(locallyOverrideFeatureFlags)
            }
        },
        setOverriddenUserFlag: ({ flagKey, overrideValue }) => {
            const clientMarketTor = values.markettor
            if (clientMarketTor) {
                clientMarketTor.featureFlags.override({ ...values.localOverrides, [flagKey]: overrideValue })
                toolbarMarkettorJS.capture('toolbar feature flag overridden')
                actions.checkLocalOverrides()
                clientMarketTor.featureFlags.reloadFeatureFlags()
            }
        },
        deleteOverriddenUserFlag: ({ flagKey }) => {
            const clientMarketTor = values.markettor
            if (clientMarketTor) {
                const updatedFlags = { ...values.localOverrides }
                delete updatedFlags[flagKey]
                if (Object.keys(updatedFlags).length > 0) {
                    clientMarketTor.featureFlags.override({ ...updatedFlags })
                } else {
                    clientMarketTor.featureFlags.override(false)
                }
                toolbarMarkettorJS.capture('toolbar feature flag override removed')
                actions.checkLocalOverrides()
                clientMarketTor.featureFlags.reloadFeatureFlags()
            }
        },
    })),
    permanentlyMount(),
])

function getGroups(markettorInstance: MarketTor | null): Record<string, any> {
    try {
        return markettorInstance?.getGroups() || {}
    } catch {
        return {}
    }
}
