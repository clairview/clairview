import type { ClairviewTranslation } from '../../../schema/translation.js';
import type { ApplyQueryFields, Query } from '../../../types/index.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

export type ReadTranslationOutput<
	Schema,
	TQuery extends Query<Schema, Item>,
	Item extends object = ClairviewTranslation<Schema>,
> = ApplyQueryFields<Schema, Item, TQuery['fields']>;

/**
 * List all Translations that exist in Clairview.
 * @param query The query parameters
 * @returns An array of up to limit Translation objects. If no items are available, data will be an empty array.
 */
export const readTranslations =
	<Schema, const TQuery extends Query<Schema, ClairviewTranslation<Schema>>>(
		query?: TQuery,
	): RestCommand<ReadTranslationOutput<Schema, TQuery>[], Schema> =>
	() => ({
		path: `/translations`,
		params: query ?? {},
		method: 'GET',
	});

/**
 * List an existing Translation by primary key.
 * @param key The primary key of the dashboard
 * @param query The query parameters
 * @returns Returns a Translation object if a valid primary key was provided.
 * @throws Will throw if key is empty
 */
export const readTranslation =
	<Schema, const TQuery extends Query<Schema, ClairviewTranslation<Schema>>>(
		key: ClairviewTranslation<Schema>['id'],
		query?: TQuery,
	): RestCommand<ReadTranslationOutput<Schema, TQuery>, Schema> =>
	() => {
		throwIfEmpty(String(key), 'Key cannot be empty');

		return {
			path: `/translations/${key}`,
			params: query ?? {},
			method: 'GET',
		};
	};
