import type { FieldMeta } from '@clairview/types';
import { systemFieldRows } from '@clairview/system-data';
import formatTitle from '@clairview/format-title';
import { getAuthProviders } from './get-auth-providers.js';

// Dynamically populate auth providers field
export function getSystemFieldRowsWithAuthProviders(): FieldMeta[] {
	return systemFieldRows.map((systemField) => {
		if (systemField.collection === 'clairview_users' && systemField.field === 'provider') {
			if (!systemField.options) systemField.options = {};

			systemField.options['choices'] = getAuthProviders().map(({ name }) => ({
				text: formatTitle(name),
				value: name,
			}));
		}

		return systemField;
	});
}
