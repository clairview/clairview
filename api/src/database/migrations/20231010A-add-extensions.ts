import type { Knex } from 'knex';

export async function up(knex: Knex): Promise<void> {
	await knex.schema.createTable('clairview_extensions', (table) => {
		table.string('name').primary().notNullable();
		table.boolean('enabled').defaultTo(true).notNullable();
	});
}

export async function down(knex: Knex): Promise<void> {
	await knex.schema.dropTable('clairview_extensions');
}
