import type { ClairviewDashboard } from '../../../schema/dashboard.js';
import type { ApplyQueryFields, Query } from '../../../types/index.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

export type ReadDashboardOutput<
	Schema,
	TQuery extends Query<Schema, Item>,
	Item extends object = ClairviewDashboard<Schema>,
> = ApplyQueryFields<Schema, Item, TQuery['fields']>;

/**
 * List all dashboards that exist in Clairview.
 * @param query The query parameters
 * @returns An array of up to limit dashboard objects. If no items are available, data will be an empty array.
 */
export const readDashboards =
	<Schema, const TQuery extends Query<Schema, ClairviewDashboard<Schema>>>(
		query?: TQuery,
	): RestCommand<ReadDashboardOutput<Schema, TQuery>[], Schema> =>
	() => ({
		path: `/dashboards`,
		params: query ?? {},
		method: 'GET',
	});

/**
 * List an existing dashboard by primary key.
 * @param key The primary key of the dashboard
 * @param query The query parameters
 * @returns Returns the requested dashboard object.
 * @throws Will throw if key is empty
 */
export const readDashboard =
	<Schema, const TQuery extends Query<Schema, ClairviewDashboard<Schema>>>(
		key: ClairviewDashboard<Schema>['id'],
		query?: TQuery,
	): RestCommand<ReadDashboardOutput<Schema, TQuery>, Schema> =>
	() => {
		throwIfEmpty(String(key), 'Key cannot be empty');

		return {
			path: `/dashboards/${key}`,
			params: query ?? {},
			method: 'GET',
		};
	};
