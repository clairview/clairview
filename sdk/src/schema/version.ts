import type { MergeCoreCollection } from '../index.js';
import type { ClairviewCollection } from './collection.js';
import type { ClairviewUser } from './user.js';

export type ClairviewVersion<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_versions',
	{
		id: string;
		key: string;
		name: string | null;
		collection: ClairviewCollection<Schema> | string;
		item: string;
		hash: string;
		date_created: 'datetime' | null;
		date_updated: 'datetime' | null;
		user_created: ClairviewUser<Schema> | string | null;
		user_updated: ClairviewUser<Schema> | string | null;
		delta: Record<string, any> | null;
	}
>;
