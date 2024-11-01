import type { Query } from '../../../index.js';
import type { ClairviewFile } from '../../../schema/file.js';
import type { RestCommand } from '../../types.js';

export type FileFormat = 'csv' | 'json' | 'xml' | 'yaml';

/**
 * Export a larger data set to a file in the File Library
 * @returns Nothing
 */
export const utilsExport =
	<Schema, TQuery extends Query<Schema, Schema[Collection]>, Collection extends keyof Schema>(
		collection: Collection,
		format: FileFormat,
		query: TQuery,
		file: Partial<ClairviewFile<Schema>>,
	): RestCommand<void, Schema> =>
	() => ({
		method: 'POST',
		path: `/utils/export/${collection as string}`,
		body: JSON.stringify({ format, query, file }),
	});
