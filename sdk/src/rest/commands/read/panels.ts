import type { ClairviewPanel } from '../../../schema/panel.js';
import type { ApplyQueryFields, Query } from '../../../types/index.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

export type ReadPanelOutput<
	Schema,
	TQuery extends Query<Schema, Item>,
	Item extends object = ClairviewPanel<Schema>,
> = ApplyQueryFields<Schema, Item, TQuery['fields']>;

/**
 * List all Panels that exist in Clairview.
 * @param query The query parameters
 * @returns An array of up to limit panel objects. If no items are available, data will be an empty array.
 */
export const readPanels =
	<Schema, const TQuery extends Query<Schema, ClairviewPanel<Schema>>>(
		query?: TQuery,
	): RestCommand<ReadPanelOutput<Schema, TQuery>[], Schema> =>
	() => ({
		path: `/panels`,
		params: query ?? {},
		method: 'GET',
	});

/**
 * List an existing panel by primary key.
 * @param key The primary key of the dashboard
 * @param query The query parameters
 * @returns Returns the requested panel object.
 * @throws Will throw if key is empty
 */
export const readPanel =
	<Schema, const TQuery extends Query<Schema, ClairviewPanel<Schema>>>(
		key: ClairviewPanel<Schema>['id'],
		query?: TQuery,
	): RestCommand<ReadPanelOutput<Schema, TQuery>, Schema> =>
	() => {
		throwIfEmpty(String(key), 'Key cannot be empty');

		return {
			path: `/panels/${key}`,
			params: query ?? {},
			method: 'GET',
		};
	};
