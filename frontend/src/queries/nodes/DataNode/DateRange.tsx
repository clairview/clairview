import { DateFilter } from 'lib/components/DateFilter/DateFilter'

import { EventsQuery, ClairQLQuery, SessionAttributionExplorerQuery } from '~/queries/schema'
import { isEventsQuery, isClairQLQuery, isSessionAttributionExplorerQuery } from '~/queries/utils'

interface DateRangeProps<Q extends EventsQuery | ClairQLQuery | SessionAttributionExplorerQuery> {
    query: Q
    setQuery?: (query: Q) => void
}
export function DateRange<Q extends EventsQuery | ClairQLQuery | SessionAttributionExplorerQuery>({
    query,
    setQuery,
}: DateRangeProps<Q>): JSX.Element | null {
    if (isEventsQuery(query)) {
        return (
            <DateFilter
                dateFrom={query.after ?? undefined}
                dateTo={query.before ?? undefined}
                onChange={(changedDateFrom, changedDateTo) => {
                    const newQuery: Q = {
                        ...query,
                        after: changedDateFrom ?? undefined,
                        before: changedDateTo ?? undefined,
                    }
                    setQuery?.(newQuery)
                }}
            />
        )
    }
    if (isClairQLQuery(query) || isSessionAttributionExplorerQuery(query)) {
        return (
            <DateFilter
                size="medium"
                dateFrom={query.filters?.dateRange?.date_from ?? undefined}
                dateTo={query.filters?.dateRange?.date_to ?? undefined}
                onChange={(changedDateFrom, changedDateTo) => {
                    const newQuery: Q = {
                        ...query,
                        filters: {
                            ...(query.filters ?? {}),
                            dateRange: {
                                date_from: changedDateFrom ?? undefined,
                                date_to: changedDateTo ?? undefined,
                            },
                        },
                    }
                    setQuery?.(newQuery)
                }}
            />
        )
    }
    return null
}
