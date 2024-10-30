import type { ClairviewDashboard } from '../../../schema/dashboard.js';
import type { ApplyQueryFields, NestedPartial, Query } from '../../../types/index.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

export type UpdateDashboardOutput<
	Schema,
	TQuery extends Query<Schema, Item>,
	Item extends object = ClairviewDashboard<Schema>,
> = ApplyQueryFields<Schema, Item, TQuery['fields']>;

/**
 * Update multiple existing dashboards.
 * @param keys
 * @param item
 * @param query
 * @returns Returns the dashboard objects for the updated dashboards.
 * @throws Will throw if keys is empty
 */
export const updateDashboards =
	<Schema, const TQuery extends Query<Schema, ClairviewDashboard<Schema>>>(
		keys: ClairviewDashboard<Schema>['id'][],
		item: Partial<ClairviewDashboard<Schema>>,
		query?: TQuery,
	): RestCommand<UpdateDashboardOutput<Schema, TQuery>[], Schema> =>
	() => {
		throwIfEmpty(keys, 'Keys cannot be empty');

		return {
			path: `/dashboards`,
			params: query ?? {},
			body: JSON.stringify({ keys, data: item }),
			method: 'PATCH',
		};
	};

/**
 * Update multiple dashboards as batch.
 * @param items
 * @param query
 * @returns Returns the dashboard objects for the updated dashboards.
 */
export const updateDashboardsBatch =
	<Schema, const TQuery extends Query<Schema, ClairviewDashboard<Schema>>>(
		items: NestedPartial<ClairviewDashboard<Schema>>[],
		query?: TQuery,
	): RestCommand<UpdateDashboardOutput<Schema, TQuery>[], Schema> =>
	() => ({
		path: `/dashboards`,
		params: query ?? {},
		body: JSON.stringify(items),
		method: 'PATCH',
	});

/**
 * Update an existing dashboard.
 * @param key
 * @param item
 * @param query
 * @returns Returns the dashboard object for the updated dashboard.
 * @throws Will throw if key is empty
 */
export const updateDashboard =
	<Schema, const TQuery extends Query<Schema, ClairviewDashboard<Schema>>>(
		key: ClairviewDashboard<Schema>['id'],
		item: Partial<ClairviewDashboard<Schema>>,
		query?: TQuery,
	): RestCommand<UpdateDashboardOutput<Schema, TQuery>, Schema> =>
	() => {
		throwIfEmpty(key, 'Key cannot be empty');

		return {
			path: `/dashboards/${key}`,
			params: query ?? {},
			body: JSON.stringify(item),
			method: 'PATCH',
		};
	};
