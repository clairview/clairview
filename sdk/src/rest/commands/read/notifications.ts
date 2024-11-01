import type { ClairviewNotification } from '../../../schema/notification.js';
import type { ApplyQueryFields, Query } from '../../../types/index.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

export type ReadNotificationOutput<
	Schema,
	TQuery extends Query<Schema, Item>,
	Item extends object = ClairviewNotification<Schema>,
> = ApplyQueryFields<Schema, Item, TQuery['fields']>;

/**
 * List all notifications that exist in Clairview.
 * @param query The query parameters
 * @returns An array of up to limit notification objects. If no items are available, data will be an empty array.
 */
export const readNotifications =
	<Schema, const TQuery extends Query<Schema, ClairviewNotification<Schema>>>(
		query?: TQuery,
	): RestCommand<ReadNotificationOutput<Schema, TQuery>[], Schema> =>
	() => ({
		path: `/notifications`,
		params: query ?? {},
		method: 'GET',
	});

/**
 * List an existing notification by primary key.
 * @param key The primary key of the dashboard
 * @param query The query parameters
 * @returns Returns the requested notification object.
 * @throws Will throw if key is empty
 */
export const readNotification =
	<Schema, const TQuery extends Query<Schema, ClairviewNotification<Schema>>>(
		key: ClairviewNotification<Schema>['id'],
		query?: TQuery,
	): RestCommand<ReadNotificationOutput<Schema, TQuery>, Schema> =>
	() => {
		throwIfEmpty(String(key), 'Key cannot be empty');

		return {
			path: `/notifications/${key}`,
			params: query ?? {},
			method: 'GET',
		};
	};
