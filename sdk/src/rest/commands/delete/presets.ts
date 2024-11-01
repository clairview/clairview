import type { ClairviewPreset } from '../../../schema/preset.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

/**
 * Delete multiple existing presets.
 * @param keys
 * @returns
 * @throws Will throw if keys is empty
 */
export const deletePresets =
	<Schema>(keys: ClairviewPreset<Schema>['id'][]): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(keys, 'Keys cannot be empty');

		return {
			path: `/presets`,
			body: JSON.stringify(keys),
			method: 'DELETE',
		};
	};

/**
 * Delete an existing preset.
 * @param key
 * @returns
 * @throws Will throw if key is empty
 */
export const deletePreset =
	<Schema>(key: ClairviewPreset<Schema>['id']): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(String(key), 'Key cannot be empty');

		return {
			path: `/presets/${key}`,
			method: 'DELETE',
		};
	};
