import type { ClairviewRelation } from '../../../schema/relation.js';
import type { ApplyQueryFields, NestedPartial, Query } from '../../../types/index.js';
import { throwIfEmpty } from '../../utils/index.js';
import type { RestCommand } from '../../types.js';

export type UpdateRelationOutput<
	Schema,
	TQuery extends Query<Schema, Item>,
	Item extends object = ClairviewRelation<Schema>,
> = ApplyQueryFields<Schema, Item, TQuery['fields']>;

/**
 * Update an existing relation.
 * @param collection
 * @param field
 * @param item
 * @param query
 * @returns Returns the relation object for the created relation.
 */
export const updateRelation =
	<Schema, const TQuery extends Query<Schema, ClairviewRelation<Schema>>>(
		collection: ClairviewRelation<Schema>['collection'],
		field: ClairviewRelation<Schema>['field'],
		item: NestedPartial<ClairviewRelation<Schema>>,
		query?: TQuery,
	): RestCommand<UpdateRelationOutput<Schema, TQuery>, Schema> =>
	() => {
		throwIfEmpty(collection, 'Collection cannot be empty');
		throwIfEmpty(field, 'Field cannot be empty');

		return {
			path: `/relations/${collection}/${field}`,
			params: query ?? {},
			body: JSON.stringify(item),
			method: 'PATCH',
		};
	};
