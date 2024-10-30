import type { RegistryDescribeResponse, RegistryListResponse } from '@clairview/extensions-registry';
import formatTitle from '@clairview/format-title';

type Extension = RegistryListResponse['data'][number] | RegistryDescribeResponse['data'];

export const formatName = (extension: Extension) => {
	let name = extension.name;

	if (name.startsWith('@')) {
		name = name.split('/')[1]!;
	}

	if (name.startsWith('clairview-extension-')) {
		name = name.substring('clairview-extension-'.length);
	}

	return formatTitle(name);
};
