import type { Knex } from 'knex';
import { set } from 'lodash-es';
import { randomUUID } from 'node:crypto';

type NewTranslationString = {
	id: string;
	key: string;
	value: string;
	language: string;
};

type OldTranslationString = {
	key?: string | null;
	translations?: Record<string, string> | null;
};

function transformStringsNewFormat(oldStrings: OldTranslationString[]): NewTranslationString[] {
	return oldStrings.reduce<NewTranslationString[]>((result, item) => {
		if (!item.key || !item.translations) return result;

		for (const [language, value] of Object.entries(item.translations)) {
			result.push({ id: randomUUID(), key: item.key, language, value });
		}

		return result;
	}, []);
}

function transformStringsOldFormat(newStrings: NewTranslationString[]): OldTranslationString[] {
	const keyCache: Record<string, Record<string, string>> = {};

	for (const { key, language, value } of newStrings) {
		set(keyCache, [key, language], value);
	}

	return Object.entries(keyCache).map(([key, translations]) => ({ key, translations }) as OldTranslationString);
}

export async function up(knex: Knex): Promise<void> {
	await knex.schema.createTable('clairview_translations', (table) => {
		table.uuid('id').primary().notNullable();
		table.string('language').notNullable();
		table.string('key').notNullable();
		table.text('value').notNullable();
	});

	const data = await knex.select('translation_strings', 'id').from('clairview_settings').first();

	if (data?.translation_strings && data?.id) {
		const parsedTranslationStrings =
			typeof data.translation_strings === 'string' ? JSON.parse(data.translation_strings) : data.translation_strings;

		const newTranslationStrings = transformStringsNewFormat(parsedTranslationStrings);

		for (const item of newTranslationStrings) {
			await knex('clairview_translations').insert(item);
		}
	}

	await knex.schema.alterTable('clairview_settings', (table) => {
		table.dropColumn('translation_strings');
	});
}

export async function down(knex: Knex): Promise<void> {
	const data = await knex.select('language', 'key', 'value').from('clairview_translations');
	const settingsId = await knex.select('id').from('clairview_settings').first();

	await knex.schema.alterTable('clairview_settings', (table) => {
		table.json('translation_strings');
	});

	if (settingsId?.id && data) {
		const oldTranslationStrings = transformStringsOldFormat(data);

		await knex('clairview_settings')
			.where({ id: settingsId.id })
			.update({
				translation_strings: JSON.stringify(oldTranslationStrings),
			});
	}

	await knex.schema.dropTable('clairview_translations');
}
