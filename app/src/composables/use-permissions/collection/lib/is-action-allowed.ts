import { usePermissionsStore } from '@/stores/permissions';
import { PermissionsAction } from '@clairview/types';
import { computed, unref } from 'vue';
import { Collection } from '../../types';

export const isActionAllowed = (collection: Collection, action: PermissionsAction) => {
	const { hasPermission } = usePermissionsStore();

	return computed(() => {
		const collectionValue = unref(collection);

		if (!collectionValue) return false;

		return hasPermission(collectionValue, action);
	});
};
