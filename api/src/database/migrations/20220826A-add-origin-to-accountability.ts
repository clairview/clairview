import type { Knex } from 'knex';

export async function up(knex: Knex): Promise<void> {
	await knex.schema.alterTable('clairview_activity', (table) => {
		table.string('origin').nullable();
	});

	await knex.schema.alterTable('clairview_sessions', (table) => {
		table.string('origin').nullable();
	});
}

export async function down(knex: Knex): Promise<void> {
	await knex.schema.alterTable('clairview_activity', (table) => {
		table.dropColumn('origin');
	});

	await knex.schema.alterTable('clairview_sessions', (table) => {
		table.dropColumn('origin');
	});
}
