import type { ClairviewDashboard } from '../../../schema/dashboard.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

/**
 * Delete multiple existing dashboards.
 * @param keysOrQuery
 * @returns
 * @throws Will throw if keys is empty
 */
export const deleteDashboards =
	<Schema>(keys: ClairviewDashboard<Schema>['id'][]): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(keys, 'Keys cannot be empty');

		return {
			path: `/dashboards`,
			body: JSON.stringify(keys),
			method: 'DELETE',
		};
	};

/**
 * Delete an existing dashboard.
 * @param key
 * @returns
 * @throws Will throw if key is empty
 */
export const deleteDashboard =
	<Schema>(key: ClairviewDashboard<Schema>['id']): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(key, 'Key cannot be empty');

		return {
			path: `/dashboards/${key}`,
			method: 'DELETE',
		};
	};
