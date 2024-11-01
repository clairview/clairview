import type { PrimaryKeyType } from './types';

export const DEFAULT_DB_TABLES = [
	'tests_flow_data',
	'tests_flow_completed',
	'clairview_activity',
	'clairview_collections',
	'clairview_dashboards',
	'clairview_fields',
	'clairview_files',
	'clairview_folders',
	'clairview_migrations',
	'clairview_notifications',
	'clairview_panels',
	'clairview_permissions',
	'clairview_presets',
	'clairview_relations',
	'clairview_revisions',
	'clairview_roles',
	'clairview_sessions',
	'clairview_settings',
	'clairview_shares',
	'clairview_users',
	'clairview_webhooks',
] as const;

// Role IDs
export const ROLE = {
	TESTS_FLOW: {
		ID: 'd70c0943-5b55-4c5d-a613-f539a27a57f5', // Created through migration
		NAME: 'Tests Flow Role',
	},
	ADMIN: {
		NAME: 'Admin Role',
	},
	APP_ACCESS: {
		NAME: 'App Access Role',
	},
	API_ONLY: {
		NAME: 'API Only Role',
	},
} as const;

type UserData = {
	ID?: string;
	TOKEN: string;
	EMAIL: string;
	PASSWORD: string;
	NAME: string;
	KEY: string;
};

type UserType = {
	[key: string]: UserData;
};

export const USER = {
	TESTS_FLOW: {
		ID: '3d075128-c073-4f5d-891c-ed2eb2790a1c', // Created through migration
		TOKEN: 'TestsFlowToken',
		EMAIL: 'flow@tests.com',
		PASSWORD: 'TestsFlowPassword',
		NAME: 'Tests Flow User',
		KEY: 'TESTS_FLOW',
	},
	ADMIN: {
		TOKEN: 'AdminToken',
		EMAIL: 'admin@default.com',
		PASSWORD: 'AdminPassword',
		NAME: 'Admin User',
		KEY: 'ADMIN',
	},
	APP_ACCESS: {
		TOKEN: 'AppAccessToken',
		EMAIL: 'app-access@default.com',
		PASSWORD: 'AppAccessPassword',
		NAME: 'App Access User',
		KEY: 'APP_ACCESS',
	},
	API_ONLY: {
		TOKEN: 'APIOnlyToken',
		EMAIL: 'api-only@default.com',
		PASSWORD: 'APIOnlyPassword',
		NAME: 'API Only User',
		KEY: 'API_ONLY',
	},
	NO_ROLE: {
		TOKEN: 'NoRoleToken',
		EMAIL: 'no-role@default.com',
		PASSWORD: 'NoRolePassword',
		NAME: 'No-Role User',
		KEY: 'NO_ROLE',
	},
} as const satisfies UserType;

export const TEST_USERS = ['ADMIN', 'APP_ACCESS', 'API_ONLY', 'NO_ROLE'] as const; // TESTS_FLOW is exluded

export const PRIMARY_KEY_TYPES = ['integer', 'uuid', 'string'] as const satisfies readonly PrimaryKeyType[];
