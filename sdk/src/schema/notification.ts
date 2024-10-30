import type { MergeCoreCollection } from '../index.js';
import type { ClairviewUser } from './user.js';

export type ClairviewNotification<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_notifications',
	{
		id: string;
		timestamp: 'datetime' | null;
		status: string | null;
		recipient: ClairviewUser<Schema> | string;
		sender: ClairviewUser<Schema> | string | null;
		subject: string;
		message: string | null;
		collection: string | null; // TODO keyof complete schema
		item: string | null;
	}
>;
