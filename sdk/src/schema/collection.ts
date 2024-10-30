import type { ClairviewField, MergeCoreCollection, NestedPartial } from '../index.js';

export type ClairviewCollection<Schema = any> = {
	collection: string; // TODO keyof complete schema
	meta: MergeCoreCollection<
		Schema,
		'clairview_collections',
		{
			collection: string; // TODO keyof complete schema
			icon: string | null;
			note: string | null;
			display_template: string | null;
			hidden: boolean;
			singleton: boolean;
			translations: CollectionMetaTranslationType[] | null;
			archive_field: string | null;
			archive_app_filter: boolean;
			archive_value: string | null;
			unarchive_value: string | null;
			sort_field: string | null;
			accountability: string | null;
			color: string | null;
			item_duplication_fields: string[] | null;
			sort: number | null;
			group: string | null;
			collapse: string;
			preview_url: string | null;
			versioning: boolean;
		}
	>;
	schema:
		| ({
				name: string;
				comment: string | null;
		  } & Record<string, unknown>)
		| null;
	fields?: NestedPartial<ClairviewField<Schema>>[];
};

export type CollectionMetaTranslationType = {
	language: string;
	plural: string;
	singular: string;
	translation: string;
};
