import type { ClairviewVersion } from '../../../schema/version.js';
import type { ApplyQueryFields, Query } from '../../../types/index.js';
import type { RestCommand } from '../../types.js';

export type CreateContentVersionOutput<
	Schema,
	TQuery extends Query<Schema, Item>,
	Item extends object = ClairviewVersion<Schema>,
> = ApplyQueryFields<Schema, Item, TQuery['fields']>;

/**
 * Create multiple new Content Versions.
 *
 * @param items The Content Versions to create
 * @param query Optional return data query
 *
 * @returns Returns the Content Version object for the created Content Versions.
 */
export const createContentVersions =
	<Schema, const TQuery extends Query<Schema, ClairviewVersion<Schema>>>(
		items: Partial<ClairviewVersion<Schema>>[],
		query?: TQuery,
	): RestCommand<CreateContentVersionOutput<Schema, TQuery>[], Schema> =>
	() => ({
		path: `/versions`,
		params: query ?? {},
		body: JSON.stringify(items),
		method: 'POST',
	});

/**
 * Create a new Content Version.
 *
 * @param item The Content Version to create
 * @param query Optional return data query
 *
 * @returns Returns the Content Version object for the created Content Version.
 */
export const createContentVersion =
	<Schema, const TQuery extends Query<Schema, ClairviewVersion<Schema>>>(
		item: Partial<ClairviewVersion<Schema>>,
		query?: TQuery,
	): RestCommand<CreateContentVersionOutput<Schema, TQuery>, Schema> =>
	() => ({
		path: `/versions`,
		params: query ?? {},
		body: JSON.stringify(item),
		method: 'POST',
	});
