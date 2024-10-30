import type { MergeCoreCollection } from '../index.js';
import type { ClairviewRole } from './role.js';
import type { ClairviewUser } from './user.js';

export type ClairviewShare<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_shares',
	{
		id: string;
		name: string | null;
		collection: string | null;
		item: string | null;
		role: ClairviewRole<Schema> | string | null;
		password: string | null;
		user_created: ClairviewUser<Schema> | string | null;
		date_created: 'datetime' | null;
		date_start: 'datetime' | null;
		date_end: 'datetime' | null;
		times_used: number | null;
		max_uses: number | null;
	}
>;
