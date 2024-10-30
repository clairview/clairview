import type { MergeCoreCollection } from '../index.js';
import type { ClairviewActivity } from './activity.js';
import type { ClairviewVersion } from './version.js';

export type ClairviewRevision<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_revisions',
	{
		id: number;
		activity: ClairviewActivity<Schema> | number;
		collection: string; // TODO keyof complete schema
		item: string;
		data: Record<string, any> | null;
		delta: Record<string, any> | null;
		parent: ClairviewRevision<Schema> | number | null;
		version: ClairviewVersion<Schema> | string | null;
	}
>;
