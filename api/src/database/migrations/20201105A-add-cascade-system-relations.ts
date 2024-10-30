import type { Knex } from 'knex';

const updates = [
	{
		table: 'clairview_fields',
		constraints: [
			{
				column: 'group',
				references: 'clairview_fields.id',
			},
		],
	},
	{
		table: 'clairview_files',
		constraints: [
			{
				column: 'folder',
				references: 'clairview_folders.id',
			},
			{
				column: 'uploaded_by',
				references: 'clairview_users.id',
			},
			{
				column: 'modified_by',
				references: 'clairview_users.id',
			},
		],
	},
	{
		table: 'clairview_folders',
		constraints: [
			{
				column: 'parent',
				references: 'clairview_folders.id',
			},
		],
	},
	{
		table: 'clairview_permissions',
		constraints: [
			{
				column: 'role',
				references: 'clairview_roles.id',
			},
		],
	},
	{
		table: 'clairview_presets',
		constraints: [
			{
				column: 'user',
				references: 'clairview_users.id',
			},
			{
				column: 'role',
				references: 'clairview_roles.id',
			},
		],
	},
	{
		table: 'clairview_revisions',
		constraints: [
			{
				column: 'activity',
				references: 'clairview_activity.id',
			},
			{
				column: 'parent',
				references: 'clairview_revisions.id',
			},
		],
	},
	{
		table: 'clairview_sessions',
		constraints: [
			{
				column: 'user',
				references: 'clairview_users.id',
			},
		],
	},
	{
		table: 'clairview_settings',
		constraints: [
			{
				column: 'project_logo',
				references: 'clairview_files.id',
			},
			{
				column: 'public_foreground',
				references: 'clairview_files.id',
			},
			{
				column: 'public_background',
				references: 'clairview_files.id',
			},
		],
	},
	{
		table: 'clairview_users',
		constraints: [
			{
				column: 'role',
				references: 'clairview_roles.id',
			},
		],
	},
];

/**
 * NOTE:
 * Not all databases allow (or support) recursive onUpdate/onDelete triggers. MS SQL / Oracle flat out deny creating them,
 * Postgres behaves erratic on those triggers, not sure if MySQL / Maria plays nice either.
 */

export async function up(knex: Knex): Promise<void> {
	for (const update of updates) {
		await knex.schema.alterTable(update.table, (table) => {
			for (const constraint of update.constraints) {
				table.dropForeign([constraint.column]);
				table.foreign(constraint.column).references(constraint.references);
			}
		});
	}
}

export async function down(knex: Knex): Promise<void> {
	for (const update of updates) {
		await knex.schema.alterTable(update.table, (table) => {
			for (const constraint of update.constraints) {
				table.dropForeign([constraint.column]);
			}
		});
	}
}
