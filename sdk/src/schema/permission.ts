import type { MergeCoreCollection } from '../index.js';
import type { ClairviewPolicy } from './policy.js';

export type ClairviewPermission<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_permissions',
	{
		id: number;
		policy: ClairviewPolicy<Schema> | string | null;
		collection: string; // TODO keyof complete schema
		action: string;
		permissions: Record<string, any> | null;
		validation: Record<string, any> | null;
		presets: Record<string, any> | null;
		fields: string[] | null;
	}
>;
