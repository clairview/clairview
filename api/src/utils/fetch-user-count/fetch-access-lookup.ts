import type { PrimaryKey } from '@clairview/types';
import type { Knex } from 'knex';

export interface AccessLookup {
	role: string | null;
	user: string | null;
	app_access: boolean | number;
	admin_access: boolean | number;
	user_status: 'active' | string;
	user_role: string | null;
}

export interface FetchAccessLookupOptions {
	excludeAccessRows?: PrimaryKey[];
	excludePolicies?: PrimaryKey[];
	excludeUsers?: PrimaryKey[];
	excludeRoles?: PrimaryKey[];
	adminOnly?: boolean;
	knex: Knex;
}

export async function fetchAccessLookup(options: FetchAccessLookupOptions): Promise<AccessLookup[]> {
	let query = options.knex
		.select(
			'clairview_access.role',
			'clairview_access.user',
			'clairview_policies.app_access',
			'clairview_policies.admin_access',
			'clairview_users.status as user_status',
			'clairview_users.role as user_role',
		)
		.from('clairview_access')
		.leftJoin('clairview_policies', 'clairview_access.policy', 'clairview_policies.id')
		.leftJoin('clairview_users', 'clairview_access.user', 'clairview_users.id');

	if (options.excludeAccessRows && options.excludeAccessRows.length > 0) {
		query = query.whereNotIn('clairview_access.id', options.excludeAccessRows);
	}

	if (options.excludePolicies && options.excludePolicies.length > 0) {
		query = query.whereNotIn('clairview_access.policy', options.excludePolicies);
	}

	if (options.excludeUsers && options.excludeUsers.length > 0) {
		query = query.where((q) =>
			q.whereNotIn('clairview_access.user', options.excludeUsers!).orWhereNull('clairview_access.user'),
		);
	}

	if (options.excludeRoles && options.excludeRoles.length > 0) {
		query = query.where((q) =>
			q.whereNotIn('clairview_access.role', options.excludeRoles!).orWhereNull('clairview_access.role'),
		);
	}

	if (options.adminOnly) {
		query = query.where('clairview_policies.admin_access', 1);
	}

	return query;
}
