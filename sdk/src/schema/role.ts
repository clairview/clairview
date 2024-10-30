import type { MergeCoreCollection } from '../index.js';
import type { ClairviewUser } from './user.js';
import type { ClairviewPolicy } from './policy.js';

export type ClairviewRole<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_roles',
	{
		id: string;
		name: string;
		icon: string;
		description: string | null;
		parent: string | ClairviewRole<Schema>;
		children: string[] | ClairviewRole<Schema>[];
		policies: string[] | ClairviewPolicy<Schema>[];
		users: string[] | ClairviewUser<Schema>[];
	}
>;
