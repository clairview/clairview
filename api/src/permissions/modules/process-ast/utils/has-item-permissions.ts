import type { Permission } from '@clairview/types';

export function hasItemPermissions(permission: Permission) {
	return permission.permissions !== null && Object.keys(permission.permissions).length > 0;
}
