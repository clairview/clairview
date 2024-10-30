import type { MergeCoreCollection } from '../index.js';
import type { ClairviewRevision } from './revision.js';
import type { ClairviewUser } from './user.js';

export type ClairviewActivity<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_activity',
	{
		id: number;
		action: string;
		user: ClairviewUser<Schema> | string | null;
		timestamp: 'datetime';
		ip: string | null;
		user_agent: string | null;
		collection: string;
		item: string;
		comment: string | null;
		origin: string | null;
		revisions: ClairviewRevision<Schema>[] | number[] | null;
	}
>;
