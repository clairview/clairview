import type { ClairviewField } from '../../../schema/field.js';
import type { ApplyQueryFields } from '../../../types/index.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

export type ReadFieldOutput<Schema, Item extends object = ClairviewField<Schema>> = ApplyQueryFields<Schema, Item, '*'>;

/**
 * List the available fields.
 * @param query The query parameters
 * @returns An array of field objects.
 */
export const readFields =
	<Schema>(): RestCommand<ReadFieldOutput<Schema>[], Schema> =>
	() => ({
		path: `/fields`,
		method: 'GET',
	});

/**
 * List the available fields in a given collection.
 * @param collection The primary key of the field
 * @returns
 * @throws Will throw if collection is empty
 */
export const readFieldsByCollection =
	<Schema>(collection: ClairviewField<Schema>['collection']): RestCommand<ReadFieldOutput<Schema>[], Schema> =>
	() => {
		throwIfEmpty(collection, 'Collection cannot be empty');

		return {
			path: `/fields/${collection}`,
			method: 'GET',
		};
	};

/**
 *
 * @param key The primary key of the dashboard
 * @param query The query parameters
 * @returns
 * @throws Will throw if collection is empty
 * @throws Will throw if field is empty
 */
export const readField =
	<Schema>(
		collection: ClairviewField<Schema>['collection'],
		field: ClairviewField<Schema>['field'],
	): RestCommand<ReadFieldOutput<Schema>, Schema> =>
	() => {
		throwIfEmpty(collection, 'Collection cannot be empty');
		throwIfEmpty(field, 'Field cannot be empty');

		return {
			path: `/fields/${collection}/${field}`,
			method: 'GET',
		};
	};
