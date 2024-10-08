import { actions, kea, path, reducers } from 'kea'

import type { userPreferencesLogicType } from './userPreferencesLogicType'

// This logic is for browser stored user preferences where it's not super important that it is persisted to the server
export const userPreferencesLogic = kea<userPreferencesLogicType>([
    path(['lib', 'logic', 'userPreferencesLogic']),
    actions({
        setHideClairViewPropertiesInTable: (enabled: boolean) => ({ enabled }),
    }),
    reducers(() => ({
        hideClairViewPropertiesInTable: [
            false,
            { persist: true },
            {
                setHideClairViewPropertiesInTable: (_, { enabled }) => enabled,
            },
        ],
    })),
])
