import type { ClairviewShare } from '../../../schema/share.js';
import type { ApplyQueryFields, NestedPartial, Query } from '../../../types/index.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

export type UpdateShareOutput<
	Schema,
	TQuery extends Query<Schema, Item>,
	Item extends object = ClairviewShare<Schema>,
> = ApplyQueryFields<Schema, Item, TQuery['fields']>;

/**
 * Update multiple existing shares.
 * @param keys
 * @param item
 * @param query
 * @returns Returns the share objects for the updated shares.
 * @throws Will throw if keys is empty
 */
export const updateShares =
	<Schema, const TQuery extends Query<Schema, ClairviewShare<Schema>>>(
		keys: ClairviewShare<Schema>['id'][],
		item: Partial<ClairviewShare<Schema>>,
		query?: TQuery,
	): RestCommand<UpdateShareOutput<Schema, TQuery>[], Schema> =>
	() => {
		throwIfEmpty(keys, 'Keys cannot be empty');

		return {
			path: `/shares`,
			params: query ?? {},
			body: JSON.stringify({ keys, data: item }),
			method: 'PATCH',
		};
	};

/**
 * Update multiple shares as batch.
 * @param items
 * @param query
 * @returns Returns the share objects for the updated shares.
 */
export const updateSharesBatch =
	<Schema, const TQuery extends Query<Schema, ClairviewShare<Schema>>>(
		items: NestedPartial<ClairviewShare<Schema>>[],
		query?: TQuery,
	): RestCommand<UpdateShareOutput<Schema, TQuery>[], Schema> =>
	() => ({
		path: `/shares`,
		params: query ?? {},
		body: JSON.stringify(items),
		method: 'PATCH',
	});

/**
 * Update an existing share.
 * @param key
 * @param item
 * @param query
 * @returns Returns the share object for the updated share.
 * @throws Will throw if key is empty
 */
export const updateShare =
	<Schema, const TQuery extends Query<Schema, ClairviewShare<Schema>>>(
		key: ClairviewShare<Schema>['id'],
		item: Partial<ClairviewShare<Schema>>,
		query?: TQuery,
	): RestCommand<UpdateShareOutput<Schema, TQuery>, Schema> =>
	() => {
		throwIfEmpty(key, 'Key cannot be empty');

		return {
			path: `/shares/${key}`,
			params: query ?? {},
			body: JSON.stringify(item),
			method: 'PATCH',
		};
	};
