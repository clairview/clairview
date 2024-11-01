import type { ClairviewRole } from '../../../schema/role.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

/**
 * Delete multiple existing roles.
 * @param keys
 * @returns
 * @throws Will throw if keys is empty
 */
export const deleteRoles =
	<Schema>(keys: ClairviewRole<Schema>['id'][]): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(keys, 'Keys cannot be empty');

		return {
			path: `/roles`,
			body: JSON.stringify(keys),
			method: 'DELETE',
		};
	};

/**
 * Delete an existing role.
 * @param key
 * @returns
 * @throws Will throw if key is empty
 */
export const deleteRole =
	<Schema>(key: ClairviewRole<Schema>['id']): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(String(key), 'Key cannot be empty');

		return {
			path: `/roles/${key}`,
			method: 'DELETE',
		};
	};
