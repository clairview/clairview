import { useExtensions } from '@/extensions';
import type { AppExtensionConfigs, AppExtensionType, HybridExtensionType } from '@clairview/extensions';
import type { Plural } from '@clairview/types';
import { pluralize } from '@clairview/utils';
import { Ref, computed, unref } from 'vue';

export function useExtension<T extends AppExtensionType | HybridExtensionType>(
	type: T | Ref<T>,
	name: string | Ref<string | null>,
): Ref<AppExtensionConfigs[Plural<T>][number] | null> {
	const extensions = useExtensions();

	return computed(() => {
		if (unref(name) === null) return null;
		return (extensions[pluralize(unref(type))].value as any[]).find(({ id }) => id === unref(name)) ?? null;
	});
}
