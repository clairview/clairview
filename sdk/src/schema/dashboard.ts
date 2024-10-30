import type { MergeCoreCollection } from '../index.js';
import type { ClairviewUser } from './user.js';

export type ClairviewDashboard<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_dashboards',
	{
		id: string;
		name: string;
		icon: string;
		note: string | null;
		date_created: 'datetime' | null;
		user_created: ClairviewUser<Schema> | string | null;
		color: string | null;
	}
>;
