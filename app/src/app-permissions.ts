import { Permission } from '@clairview/types';

export const appRecommendedPermissions: Partial<Permission>[] = [
	{
		collection: 'clairview_comments',
		action: 'read',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_files',
		action: 'create',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_files',
		action: 'read',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_files',
		action: 'update',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_files',
		action: 'delete',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_dashboards',
		action: 'create',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_dashboards',
		action: 'read',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_dashboards',
		action: 'update',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_dashboards',
		action: 'delete',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_panels',
		action: 'create',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_panels',
		action: 'read',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_panels',
		action: 'update',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_panels',
		action: 'delete',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_folders',
		action: 'create',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_folders',
		action: 'read',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_folders',
		action: 'update',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_folders',
		action: 'delete',
		permissions: {},
	},
	{
		collection: 'clairview_users',
		action: 'read',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_users',
		action: 'update',
		permissions: {
			id: {
				_eq: '$CURRENT_USER',
			},
		},
		fields: [
			'first_name',
			'last_name',
			'email',
			'password',
			'location',
			'title',
			'description',
			'avatar',
			'language',
			'appearance',
			'theme_light',
			'theme_dark',
			'theme_light_overrides',
			'theme_dark_overrides',
			'tfa_secret',
		],
	},
	{
		collection: 'clairview_roles',
		action: 'read',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_shares',
		action: 'read',
		permissions: {
			_or: [
				{
					// TODO should this be _in $CURRENT_ROLES?
					role: {
						_eq: '$CURRENT_ROLE',
					},
				},
				{
					role: {
						_null: true,
					},
				},
			],
		},
		fields: ['*'],
	},
	{
		collection: 'clairview_shares',
		action: 'create',
		permissions: {},
		fields: ['*'],
	},
	{
		collection: 'clairview_shares',
		action: 'update',
		permissions: {
			user_created: {
				_eq: '$CURRENT_USER',
			},
		},
		fields: ['*'],
	},
	{
		collection: 'clairview_shares',
		action: 'delete',
		permissions: {
			user_created: {
				_eq: '$CURRENT_USER',
			},
		},
		fields: ['*'],
	},
	{
		collection: 'clairview_flows',
		action: 'read',
		permissions: {
			trigger: {
				_eq: 'manual',
			},
		},
		fields: ['id', 'status', 'name', 'icon', 'color', 'options', 'trigger'],
	},
];

export const editablePermissionActions = ['create', 'read', 'update', 'delete', 'share'] as const;
export type EditablePermissionsAction = (typeof editablePermissionActions)[number];

export const disabledActions: Record<string, EditablePermissionsAction[]> = {
	clairview_extensions: ['create', 'delete'],
};
