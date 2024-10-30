import type { ExtensionOptionsBundleEntry } from '@clairview/extensions';
import { API_EXTENSION_TYPES, APP_EXTENSION_TYPES, HYBRID_EXTENSION_TYPES } from '@clairview/extensions';
import { isIn, isTypeIn, pluralize } from '@clairview/utils';
import { pathToRelativeUrl } from '@clairview/utils/node';
import path from 'path';

export default function generateBundleEntrypoint(mode: 'app' | 'api', entries: ExtensionOptionsBundleEntry[]): string {
	const types = [...(mode === 'app' ? APP_EXTENSION_TYPES : API_EXTENSION_TYPES), ...HYBRID_EXTENSION_TYPES];

	const entriesForTypes = entries.filter((entry) => isIn(entry.type, types));

	const imports = entriesForTypes.map((entry, index) => {
		let entryPath: string;

		if (isTypeIn(entry, HYBRID_EXTENSION_TYPES)) {
			entryPath = mode === 'app' ? entry.source.app : entry.source.api;
		} else {
			entryPath = entry.source;
		}

		return `import e${index} from './${pathToRelativeUrl(path.resolve(entryPath))}';`;
	});

	const exports = types.map((type) => {
		const entries = entriesForTypes.reduce<string[]>((result, entry, index) => {
			if (entry.type !== type) return result;

			if (mode === 'app') {
				result.push(`e${index}`);
			} else {
				result.push(`{name:'${entry.name}',config:e${index}}`);
			}

			return result;
		}, []);

		return `export const ${pluralize(type)} = [${entries.join(',')}];`;
	});

	return `${imports.join('')}${exports.join('')}`;
}
