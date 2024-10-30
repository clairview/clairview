import type { MergeCoreCollection } from '../index.js';
import type { ClairviewPermission } from './permission.js';
import type { ClairviewRole } from './role.js';
import type { ClairviewUser } from './user.js';

export type ClairviewPolicy<Schema> = MergeCoreCollection<
	Schema,
	'clairview_policies',
	{
		id: string; // uuid
		name: string;
		icon: string;
		description: string | null;
		ip_access: string | null;
		enforce_tfa: boolean;
		admin_access: boolean;
		app_access: boolean;
		permissions: number[] | ClairviewPermission<Schema>[];
		users: string[] | ClairviewUser<Schema>[];
		roles: string[] | ClairviewRole<Schema>[];
	}
>;
