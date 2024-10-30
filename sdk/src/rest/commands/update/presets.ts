import type { ClairviewPreset } from '../../../schema/preset.js';
import type { ApplyQueryFields, NestedPartial, Query } from '../../../types/index.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

export type UpdatePresetOutput<
	Schema,
	TQuery extends Query<Schema, Item>,
	Item extends object = ClairviewPreset<Schema>,
> = ApplyQueryFields<Schema, Item, TQuery['fields']>;

/**
 * Update multiple existing presets.
 * @param keys
 * @param item
 * @param query
 * @returns Returns the preset objects for the updated presets.
 * @throws Will throw if keys is empty
 */
export const updatePresets =
	<Schema, const TQuery extends Query<Schema, ClairviewPreset<Schema>>>(
		keys: ClairviewPreset<Schema>['id'][],
		item: Partial<ClairviewPreset<Schema>>,
		query?: TQuery,
	): RestCommand<UpdatePresetOutput<Schema, TQuery>[], Schema> =>
	() => {
		throwIfEmpty(keys, 'Keys cannot be empty');

		return {
			path: `/presets`,
			params: query ?? {},
			body: JSON.stringify({ keys, data: item }),
			method: 'PATCH',
		};
	};

/**
 * Update multiple presets as batch.
 * @param items
 * @param query
 * @returns Returns the preset objects for the updated presets.
 */
export const updatePresetsBatch =
	<Schema, const TQuery extends Query<Schema, ClairviewPreset<Schema>>>(
		items: NestedPartial<ClairviewPreset<Schema>>[],
		query?: TQuery,
	): RestCommand<UpdatePresetOutput<Schema, TQuery>[], Schema> =>
	() => ({
		path: `/presets`,
		params: query ?? {},
		body: JSON.stringify(items),
		method: 'PATCH',
	});

/**
 * Update an existing preset.
 * @param key
 * @param item
 * @param query
 * @returns Returns the preset object for the updated preset.
 * @throws Will throw if key is empty
 */
export const updatePreset =
	<Schema, const TQuery extends Query<Schema, ClairviewPreset<Schema>>>(
		key: ClairviewPreset<Schema>['id'],
		item: Partial<ClairviewPreset<Schema>>,
		query?: TQuery,
	): RestCommand<UpdatePresetOutput<Schema, TQuery>, Schema> =>
	() => {
		throwIfEmpty(String(key), 'Key cannot be empty');

		return {
			path: `/presets/${key}`,
			params: query ?? {},
			body: JSON.stringify(item),
			method: 'PATCH',
		};
	};
