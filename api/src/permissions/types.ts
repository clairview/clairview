import type { SchemaOverview } from '@clairview/types';
import type { Knex } from 'knex';

export interface Context {
	schema: SchemaOverview;
	knex: Knex;
}
