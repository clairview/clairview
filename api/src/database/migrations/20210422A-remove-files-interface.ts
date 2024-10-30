import type { Knex } from 'knex';

export async function up(knex: Knex): Promise<void> {
	await knex('clairview_fields').update({ interface: 'many-to-many' }).where({ interface: 'files' });
}

export async function down(_knex: Knex): Promise<void> {
	// Do nothing
}
