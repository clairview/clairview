import type { RestCommand } from '../../types.js';

// TODO improve typing
export type SchemaSnapshotOutput = {
	version: number;
	clairview: string;
	vendor: string;
	collections: Record<string, any>[];
	fields: Record<string, any>[];
	relations: Record<string, any>[];
};

/**
 * Retrieve the current schema. This endpoint is only available to admin users.
 * @returns Returns the JSON object containing schema details.
 */
export const schemaSnapshot =
	<Schema>(): RestCommand<SchemaSnapshotOutput, Schema> =>
	() => ({
		method: 'GET',
		path: '/schema/snapshot',
	});
