import { parseJSON } from '@clairview/utils';
import type { Knex } from 'knex';

export async function up(knex: Knex): Promise<void> {
	const groups = await knex.select('*').from('clairview_fields').where({ interface: 'group-standard' });

	const raw = [];
	const detail = [];

	for (const group of groups) {
		const options = typeof group.options === 'string' ? parseJSON(group.options) : group.options || {};

		if (options.showHeader === true) {
			detail.push(group);
		} else {
			raw.push(group);
		}
	}

	for (const field of raw) {
		await knex('clairview_fields').update({ interface: 'group-raw' }).where({ id: field.id });
	}

	for (const field of detail) {
		await knex('clairview_fields').update({ interface: 'group-detail' }).where({ id: field.id });
	}
}

export async function down(knex: Knex): Promise<void> {
	await knex('clairview_fields')
		.update({
			interface: 'group-standard',
		})
		.where({ interface: 'group-detail' })
		.orWhere({ interface: 'group-raw' });
}
