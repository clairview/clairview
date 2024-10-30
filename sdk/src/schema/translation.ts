import type { MergeCoreCollection } from '../index.js';

export type ClairviewTranslation<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_translations',
	{
		id: string; // uuid
		language: string;
		key: string;
		value: string;
	}
>;
