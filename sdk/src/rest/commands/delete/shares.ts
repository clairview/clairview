import type { ClairviewShare } from '../../../schema/share.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

/**
 * Delete multiple existing shares.
 * @param keys
 * @returns
 * @throws Will throw if keys is empty
 */
export const deleteShares =
	<Schema>(keys: ClairviewShare<Schema>['id'][]): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(keys, 'Keys cannot be empty');

		return {
			path: `/shares`,
			body: JSON.stringify(keys),
			method: 'DELETE',
		};
	};

/**
 * Delete an existing share.
 * @param key
 * @returns
 * @throws Will throw if key is empty
 */
export const deleteShare =
	<Schema>(key: ClairviewShare<Schema>['id']): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(String(key), 'Key cannot be empty');

		return {
			path: `/shares/${key}`,
			method: 'DELETE',
		};
	};
