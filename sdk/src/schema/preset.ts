import type { MergeCoreCollection } from '../index.js';
import type { ClairviewRole } from './role.js';
import type { ClairviewUser } from './user.js';

export type ClairviewPreset<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_presets',
	{
		id: number;
		bookmark: string | null;
		user: ClairviewUser<Schema> | string | null;
		role: ClairviewRole<Schema> | string | null;
		collection: string | null; // TODO keyof complete schema
		search: string | null;
		layout: string | null;
		layout_query: Record<string, any> | null;
		layout_options: Record<string, any> | null;
		refresh_interval: number | null;
		filter: Record<string, any> | null;
		icon: string | null;
		color: string | null;
	}
>;
