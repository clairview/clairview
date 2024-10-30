import { appAccessMinimalPermissions } from '@clairview/system-data';
import type { Accountability, Permission, Query } from '@clairview/types';
import { cloneDeep } from 'lodash-es';
import { filterItems } from '../../utils/filter-items.js';

export function withAppMinimalPermissions(
	accountability: Pick<Accountability, 'app'> | null,
	permissions: Permission[],
	filter: Query['filter'],
): Permission[] {
	if (accountability?.app === true) {
		const filteredAppMinimalPermissions = cloneDeep(filterItems(appAccessMinimalPermissions, filter));
		return [...permissions, ...filteredAppMinimalPermissions];
	}

	return permissions;
}
