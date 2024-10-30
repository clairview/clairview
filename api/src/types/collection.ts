import type { Field } from '@clairview/types';
import type { Table } from '@clairview/schema';
import type { BaseCollectionMeta } from '@clairview/system-data';

export type Collection = {
	collection: string;
	fields?: Field[];
	meta: BaseCollectionMeta | null;
	schema: Table | null;
};
