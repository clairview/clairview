import type { MergeCoreCollection } from '../index.js';
import type { ClairviewUser } from './user.js';
import type { ClairviewDashboard } from './dashboard.js';

export type ClairviewPanel<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_panels',
	{
		id: string;
		dashboard: ClairviewDashboard<Schema> | string;
		name: string | null;
		icon: string | null;
		color: string | null;
		show_header: boolean;
		note: string | null;
		type: string;
		position_x: number;
		position_y: number;
		width: number;
		height: number;
		options: Record<string, any> | null;
		date_created: 'datetime' | null;
		user_created: ClairviewUser<Schema> | string | null;
	}
>;
