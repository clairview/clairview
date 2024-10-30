import type { ClairviewPreset } from '../../../schema/preset.js';
import type { ApplyQueryFields, Query } from '../../../types/index.js';
import type { RestCommand } from '../../types.js';

export type CreatePresetOutput<
	Schema,
	TQuery extends Query<Schema, Item>,
	Item extends object = ClairviewPreset<Schema>,
> = ApplyQueryFields<Schema, Item, TQuery['fields']>;

/**
 * Create multiple new presets.
 *
 * @param items The presets to create
 * @param query Optional return data query
 *
 * @returns Returns the preset object for the created preset.
 */
export const createPresets =
	<Schema, const TQuery extends Query<Schema, ClairviewPreset<Schema>>>(
		items: Partial<ClairviewPreset<Schema>>[],
		query?: TQuery,
	): RestCommand<CreatePresetOutput<Schema, TQuery>[], Schema> =>
	() => ({
		path: `/presets`,
		params: query ?? {},
		body: JSON.stringify(items),
		method: 'POST',
	});

/**
 * Create a new preset.
 *
 * @param item The preset to create
 * @param query Optional return data query
 *
 * @returns Returns the preset object for the created preset.
 */
export const createPreset =
	<Schema, const TQuery extends Query<Schema, ClairviewPreset<Schema>>>(
		item: Partial<ClairviewPreset<Schema>>,
		query?: TQuery,
	): RestCommand<CreatePresetOutput<Schema, TQuery>, Schema> =>
	() => ({
		path: `/presets`,
		params: query ?? {},
		body: JSON.stringify(item),
		method: 'POST',
	});
