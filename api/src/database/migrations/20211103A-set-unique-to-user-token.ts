import type { Knex } from 'knex';

export async function up(knex: Knex): Promise<void> {
	await knex.schema.alterTable('clairview_users', (table) => {
		table.unique(['token']);
	});
}

export async function down(knex: Knex): Promise<void> {
	await knex.schema.alterTable('clairview_users', (table) => {
		table.dropUnique(['token']);
	});
}
