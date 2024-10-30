import type { Accountability, Policy } from '@clairview/types';
import { toBoolean, toArray } from '@clairview/utils';
import type { Knex } from 'knex';
import { ipInNetworks } from '../../../../utils/ip-in-networks.js';
import type { GlobalAccess } from '../types.js';

type AccessRow = {
	admin_access: Policy['admin_access'] | null;
	app_access: Policy['app_access'] | null;
	ip_access: Policy['ip_access'] | string | null;
};

export async function fetchGlobalAccessForQuery(
	query: Knex.QueryBuilder<any, any[]>,
	accountability: Pick<Accountability, 'ip'>,
): Promise<GlobalAccess> {
	const globalAccess = {
		app: false,
		admin: false,
	};

	const accessRows = await query
		.select<AccessRow[]>(
			'clairview_policies.admin_access',
			'clairview_policies.app_access',
			'clairview_policies.ip_access',
		)
		.from('clairview_access')
		// @NOTE: `where` clause comes from the caller
		.leftJoin('clairview_policies', 'clairview_policies.id', 'clairview_access.policy');

	// Additively merge access permissions
	for (const { admin_access, app_access, ip_access } of accessRows) {
		if (accountability.ip && ip_access) {
			// Skip row if IP is not in the allowed networks
			const networks = toArray(ip_access);
			if (!ipInNetworks(accountability.ip, networks)) continue;
		}

		globalAccess.admin ||= toBoolean(admin_access);
		globalAccess.app ||= globalAccess.admin || toBoolean(app_access);
		if (globalAccess.admin) break;
	}

	return globalAccess;
}
