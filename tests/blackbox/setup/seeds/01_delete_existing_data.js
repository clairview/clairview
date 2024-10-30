export async function seed(knex) {
	if (process.env.TEST_LOCAL) {
		await knex('clairview_collections').del();
		await knex('clairview_relations').del();
		await knex('clairview_roles').del();
		await knex('clairview_users').del();
	}
}
