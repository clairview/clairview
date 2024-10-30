import type { MergeCoreCollection } from '../index.js';
import type { ClairviewUser } from './user.js';
import type { ClairviewOperation } from './operation.js';

export type ClairviewFlow<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_flows',
	{
		id: string;
		name: string;
		icon: string | null;
		color: string | null;
		description: string | null;
		status: string;
		trigger: string | null;
		accountability: string | null;
		options: Record<string, any> | null;
		operation: ClairviewOperation<Schema> | string | null;
		date_created: 'datetime' | null;
		user_created: ClairviewUser<Schema> | string | null;
	}
>;
