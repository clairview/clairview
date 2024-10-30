import type { MergeCoreCollection } from '../index.js';
import type { ClairviewCollection } from './collection.js';
import type { ClairviewUser } from './user.js';

export type ClairviewComment<Schema> = MergeCoreCollection<
	Schema,
	'clairview_comments',
	{
		id: string;
		collection: ClairviewCollection<Schema> | string;
		item: string;
		comment: string;
		date_created: 'datetime' | null;
		date_updated: 'datetime' | null;
		user_created: ClairviewUser<Schema> | string | null;
		user_updated: ClairviewUser<Schema> | string | null;
	}
>;
