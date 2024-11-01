import type { Knex } from 'knex';

export async function up(knex: Knex): Promise<void> {
	await knex.schema.alterTable('clairview_settings', (table) => {
		table.string('project_descriptor', 100).nullable();
	});
}

export async function down(knex: Knex): Promise<void> {
	await knex.schema.alterTable('clairview_settings', (table) => {
		table.dropColumn('project_descriptor');
	});
}
