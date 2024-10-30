import type { ClairviewComment } from '../../../schema/comment.js';
import type { ApplyQueryFields, Query } from '../../../types/index.js';
import type { RestCommand } from '../../types.js';
import { throwIfEmpty } from '../../utils/index.js';

export type ReadCommentOutput<
	Schema,
	TQuery extends Query<Schema, Item>,
	Item extends object = ClairviewComment<Schema>,
> = ApplyQueryFields<Schema, Item, TQuery['fields']>;

/**
 * List all Comments that exist in Clairview.
 * @param query The query parameters
 * @returns An array of up to limit Comment objects. If no items are available, data will be an empty array.
 */
export const readComments =
	<Schema, const TQuery extends Query<Schema, ClairviewComment<Schema>>>(
		query?: TQuery,
	): RestCommand<ReadCommentOutput<Schema, TQuery>[], Schema> =>
	() => ({
		path: `/comments`,
		params: query ?? {},
		method: 'GET',
	});

/**
 * List an existing comment by primary key.
 * @param key The primary key of the dashboard
 * @param query The query parameters
 * @returns Returns a Comment object if a valid primary key was provided.
 * @throws Will throw if key is empty
 */
export const readComment =
	<Schema, const TQuery extends Query<Schema, ClairviewComment<Schema>>>(
		key: ClairviewComment<Schema>['id'],
		query?: TQuery,
	): RestCommand<ReadCommentOutput<Schema, TQuery>, Schema> =>
	() => {
		throwIfEmpty(String(key), 'Key cannot be empty');

		return {
			path: `/comments/${key}`,
			params: query ?? {},
			method: 'GET',
		};
	};
