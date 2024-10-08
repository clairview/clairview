import Fuse from 'fuse.js'
import { actions, connect, kea, listeners, path, reducers, selectors } from 'kea'
import { loaders } from 'kea-loaders'
import { encodeParams } from 'kea-router'
import { permanentlyMount } from 'lib/utils/kea-logic-builders'
import type { ClairView } from 'clairview-js'

import { toolbarConfigLogic, toolbarFetch } from '~/toolbar/toolbarConfigLogic'
import { toolbarMarkettorJS } from '~/toolbar/toolbarMarkettorJS'
import { CombinedFeatureFlagAndValueType } from '~/types'

import type { flagsToolbarLogicType } from './flagsToolbarLogicType'

export const flagsToolbarLogic = kea<flagsToolbarLogicType>([
    path(['toolbar', 'flags', 'flagsToolbarLogic']),
    connect(() => ({
        values: [toolbarConfigLogic, ['clairview']],
    })),
    actions({
        getUserFlags: true,
        setFeatureFlagValueFromClairViewClient: (flags: string[], variants: Record<string, string | boolean>) => ({
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
                        groups: getGroups(values.clairview),
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
        clairviewClientFlagValues: [
            {} as Record<string, string | boolean>,
            {
                setFeatureFlagValueFromClairViewClient: (_, { variants }) => {
                    return variants
                },
            },
        ],
    }),
    selectors({
        userFlagsWithOverrideInfo: [
            (s) => [s.userFlags, s.localOverrides, s.clairviewClientFlagValues],
            (userFlags, localOverrides, clairviewClientFlagValues) => {
                return userFlags.map((flag) => {
                    const hasVariants = (flag.feature_flag.filters?.multivariate?.variants?.length || 0) > 0

                    const currentValue =
                        flag.feature_flag.key in localOverrides
                            ? localOverrides[flag.feature_flag.key]
                            : clairviewClientFlagValues[flag.feature_flag.key] ?? flag.value

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
            const clientClairView = values.clairview
            if (clientClairView) {
                const locallyOverrideFeatureFlags = clientClairView.get_property('$override_feature_flags') || {}
                actions.storeLocalOverrides(locallyOverrideFeatureFlags)
            }
        },
        setOverriddenUserFlag: ({ flagKey, overrideValue }) => {
            const clientClairView = values.clairview
            if (clientClairView) {
                clientClairView.featureFlags.override({ ...values.localOverrides, [flagKey]: overrideValue })
                toolbarMarkettorJS.capture('toolbar feature flag overridden')
                actions.checkLocalOverrides()
                clientClairView.featureFlags.reloadFeatureFlags()
            }
        },
        deleteOverriddenUserFlag: ({ flagKey }) => {
            const clientClairView = values.clairview
            if (clientClairView) {
                const updatedFlags = { ...values.localOverrides }
                delete updatedFlags[flagKey]
                if (Object.keys(updatedFlags).length > 0) {
                    clientClairView.featureFlags.override({ ...updatedFlags })
                } else {
                    clientClairView.featureFlags.override(false)
                }
                toolbarMarkettorJS.capture('toolbar feature flag override removed')
                actions.checkLocalOverrides()
                clientClairView.featureFlags.reloadFeatureFlags()
            }
        },
    })),
    permanentlyMount(),
])

function getGroups(clairviewInstance: ClairView | null): Record<string, any> {
    try {
        return clairviewInstance?.getGroups() || {}
    } catch {
        return {}
    }
}
