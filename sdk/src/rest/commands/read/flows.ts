import type { ClairviewFlow } from '../../../schema/flow.js';
import type { ApplyQueryFields, Query } from '../../../types/index.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

export type ReadFlowOutput<
	Schema,
	TQuery extends Query<Schema, Item>,
	Item extends object = ClairviewFlow<Schema>,
> = ApplyQueryFields<Schema, Item, TQuery['fields']>;

/**
 * List all flows that exist in Clairview.
 * @param query The query parameters
 * @returns An array of up to limit flow objects. If no items are available, data will be an empty array.
 */
export const readFlows =
	<Schema, const TQuery extends Query<Schema, ClairviewFlow<Schema>>>(
		query?: TQuery,
	): RestCommand<ReadFlowOutput<Schema, TQuery>[], Schema> =>
	() => ({
		path: `/flows`,
		params: query ?? {},
		method: 'GET',
	});

/**
 * List an existing flow by primary key.
 * @param key The primary key of the dashboard
 * @param query The query parameters
 * @returns Returns the requested flow object.
 * @throws Will throw if key is empty
 */
export const readFlow =
	<Schema, const TQuery extends Query<Schema, ClairviewFlow<Schema>>>(
		key: ClairviewFlow<Schema>['id'],
		query?: TQuery,
	): RestCommand<ReadFlowOutput<Schema, TQuery>, Schema> =>
	() => {
		throwIfEmpty(String(key), 'Key cannot be empty');

		return {
			path: `/flows/${key}`,
			params: query ?? {},
			method: 'GET',
		};
	};
