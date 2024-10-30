import type { Knex } from 'knex';

export async function up(knex: Knex): Promise<void> {
	await knex.schema.alterTable('clairview_permissions', (table) => {
		table.dropColumn('limit');
	});
}

export async function down(knex: Knex): Promise<void> {
	await knex.schema.alterTable('clairview_permissions', (table) => {
		table.integer('limit').unsigned();
	});
}
