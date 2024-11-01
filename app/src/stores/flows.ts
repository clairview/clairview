import { usePermissionsStore } from '@/stores/permissions';
import { fetchAll } from '@/utils/fetch-all';
import type { FlowRaw } from '@clairview/types';
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useFlowsStore = defineStore('flowsStore', () => {
	const flows = ref<FlowRaw[]>([]);

	return {
		flows,
		hydrate,
		dehydrate,
		getManualFlowsForCollection,
	};

	async function hydrate() {
		const { hasPermission } = usePermissionsStore();

		if (!hasPermission('clairview_flows', 'read')) {
			flows.value = [];
		} else {
			try {
				flows.value = await fetchAll('/flows', {
					params: { fields: ['*', 'operations.*'] },
				});
			} catch {
				flows.value = [];
			}
		}
	}

	async function dehydrate() {
		flows.value = [];
	}

	function getManualFlowsForCollection(collection: string): FlowRaw[] {
		return flows.value.filter(
			(flow) =>
				flow.trigger === 'manual' && flow.status === 'active' && flow.options?.collections?.includes(collection),
		);
	}
});
