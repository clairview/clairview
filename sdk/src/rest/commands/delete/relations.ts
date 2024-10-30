import type { ClairviewRelation } from '../../../schema/relation.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

/**
 * Delete an existing relation.
 * @param collection
 * @param field
 * @returns
 * @throws Will throw if collection is empty
 * @throws Will throw if field is empty
 */
export const deleteRelation =
	<Schema>(
		collection: ClairviewRelation<Schema>['collection'],
		field: ClairviewRelation<Schema>['field'],
	): RestCommand<void, Schema> =>
	() => {
		throwIfEmpty(collection, 'Collection cannot be empty');
		throwIfEmpty(field, 'Field cannot be empty');

		return {
			path: `/relations/${collection}/${field}`,
			method: 'DELETE',
		};
	};
