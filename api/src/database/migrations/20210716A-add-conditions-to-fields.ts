import type { Knex } from 'knex';

export async function up(knex: Knex): Promise<void> {
	await knex.schema.alterTable('clairview_fields', (table) => {
		table.json('conditions');
	});
}

export async function down(knex: Knex): Promise<void> {
	await knex.schema.alterTable('clairview_fields', (table) => {
		table.dropColumn('conditions');
	});
}
