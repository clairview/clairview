import type { MergeCoreCollection } from '../index.js';
import type { ClairviewFlow } from './flow.js';
import type { ClairviewUser } from './user.js';

export type ClairviewOperation<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_operations',
	{
		id: string;
		name: string | null;
		key: string;
		type: string;
		position_x: number;
		position_y: number;
		timestamp: string;
		options: Record<string, any> | null;
		resolve: ClairviewOperation<Schema> | string | null;
		reject: ClairviewOperation<Schema> | string | null;
		flow: ClairviewFlow<Schema> | string;
		date_created: 'datetime' | null;
		user_created: ClairviewUser<Schema> | string | null;
	}
>;
