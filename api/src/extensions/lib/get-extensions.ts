import { useEnv } from '@clairview/env';
import { resolveFsExtensions, resolveModuleExtensions } from '@clairview/extensions/node';
import { join } from 'node:path';
import { getExtensionsPath } from './get-extensions-path.js';

export const getExtensions = async () => {
	const env = useEnv();

	const localExtensions = await resolveFsExtensions(getExtensionsPath());
	const registryExtensions = await resolveFsExtensions(join(getExtensionsPath(), '.registry'));

	/** Extensions that are listed as dependencies in the root package.json */
	const moduleExtensions = await resolveModuleExtensions(env['PACKAGE_FILE_LOCATION'] as string);

	return { local: localExtensions, registry: registryExtensions, module: moduleExtensions };
};
