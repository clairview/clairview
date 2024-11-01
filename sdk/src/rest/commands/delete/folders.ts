import type { ClairviewFolder } from '../../../schema/folder.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

/**
 * Delete multiple existing folders.
 * @param keys
 * @returns
 * @throws Will throw if keys is empty
 */
export const deleteFolders =
	<Schema>(keys: ClairviewFolder<Schema>['id'][]): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(keys, 'Keys cannot be empty');

		return {
			path: `/folders`,
			body: JSON.stringify(keys),
			method: 'DELETE',
		};
	};

/**
 * Delete an existing folder.
 * @param key
 * @returns
 * @throws Will throw if key is empty
 */
export const deleteFolder =
	<Schema>(key: ClairviewFolder<Schema>['id']): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(key, 'Key cannot be empty');

		return {
			path: `/folders/${key}`,
			method: 'DELETE',
		};
	};
