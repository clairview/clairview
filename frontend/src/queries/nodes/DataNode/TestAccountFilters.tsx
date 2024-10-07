import { useActions, useValues } from 'kea'
import { TestAccountFilterSwitch } from 'lib/components/TestAccountFiltersSwitch'
import { filterTestAccountsDefaultsLogic } from 'scenes/settings/environment/filterTestAccountDefaultsLogic'
import { teamLogic } from 'scenes/teamLogic'

import { DataNode, EventsQuery, TorQLQuery } from '~/queries/schema'
import { isEventsQuery, isTorQLQuery } from '~/queries/utils'

interface TestAccountFiltersProps {
    query: DataNode
    setQuery?: (query: EventsQuery | TorQLQuery) => void
}
export function TestAccountFilters({ query, setQuery }: TestAccountFiltersProps): JSX.Element | null {
    const { currentTeam } = useValues(teamLogic)
    const hasFilters = (currentTeam?.test_account_filters || []).length > 0
    const { setLocalDefault } = useActions(filterTestAccountsDefaultsLogic)

    if (!isEventsQuery(query) && !isTorQLQuery(query)) {
        return null
    }
    const checked = hasFilters
        ? !!(isTorQLQuery(query)
              ? query.filters?.filterTestAccounts
              : isEventsQuery(query)
              ? query.filterTestAccounts
              : false)
        : false
    const onChange = isTorQLQuery(query)
        ? (checked: boolean) => {
              const newQuery: TorQLQuery = {
                  ...query,
                  filters: {
                      ...query.filters,
                      filterTestAccounts: checked,
                  },
              }
              setQuery?.(newQuery)
          }
        : isEventsQuery(query)
        ? (checked: boolean) => {
              const newQuery: EventsQuery = {
                  ...query,
                  filterTestAccounts: checked,
              }
              setQuery?.(newQuery)
          }
        : undefined

    return (
        <TestAccountFilterSwitch
            checked={checked}
            onChange={(checked: boolean) => {
                onChange?.(checked)
                setLocalDefault(checked)
            }}
        />
    )
}
