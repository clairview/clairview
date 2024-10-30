import type { MergeCoreCollection } from '../index.js';

export type ClairviewFolder<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_folders',
	{
		id: string;
		name: string;
		parent: ClairviewFolder<Schema> | string | null;
	}
>;
