import { usePermissionsStore } from '@/stores/permissions';
import { useUserStore } from '@/stores/user';
import { ItemPermissions } from '@clairview/types';
import { Ref, computed, unref } from 'vue';
import { Collection, IsNew } from '../../types';
import { isFullPermission } from '../utils/is-full-permission';

export const isActionAllowed = (
	collection: Collection,
	isNew: IsNew,
	fetchedItemPermissions: Ref<ItemPermissions>,
	action: 'update' | 'delete' | 'share',
) => {
	const userStore = useUserStore();
	const { getPermission } = usePermissionsStore();

	const localPermissions = computed(() => {
		const collectionValue = unref(collection);

		if (!collectionValue) return false;

		if (unref(isNew)) return false;

		if (userStore.isAdmin) return true;

		const permission = getPermission(collectionValue, action);
		if (!permission) return false;

		if (isFullPermission(permission)) return true;

		return null;
	});

	return computed(() => {
		if (localPermissions.value !== null) return localPermissions.value;

		return fetchedItemPermissions.value[action].access;
	});
};
