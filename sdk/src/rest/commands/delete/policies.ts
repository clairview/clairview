import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';
import type { ClairviewPolicy } from '../../../schema/policy.js';

/**
 * Delete multiple existing policies
 * @param keys
 * @returns
 * @throws Will throw if keys is empty
 */
export const deletePolicies =
	<Schema>(keys: ClairviewPolicy<Schema>['id'][]): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(keys, 'Keys cannot be empty');

		return {
			path: `/policies`,
			body: JSON.stringify(keys),
			method: 'DELETE',
		};
	};

/**
 * Delete an existing policy
 * @param key
 * @returns
 * @throws Will throw if key is empty
 */
export const deletePolicy =
	<Schema>(key: ClairviewPolicy<Schema>['id']): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(String(key), 'Key cannot be empty');

		return {
			path: `/policies/${key}`,
			method: 'DELETE',
		};
	};
