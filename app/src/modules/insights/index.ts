import InsightsOverview from './routes/overview.vue';
import InsightsDashboard from './routes/dashboard.vue';
import InsightsPanelConfiguration from './routes/panel-configuration.vue';
import { defineModule } from '@clairview/extensions';
import { useInsightsStore } from '@/stores/insights';

export default defineModule({
	id: 'insights',
	name: '$t:insights',
	icon: 'insights',
	routes: [
		{
			name: 'insights-overview',
			path: '',
			component: InsightsOverview,
		},
		{
			name: 'insights-dashboard',
			path: ':primaryKey',
			component: InsightsDashboard,
			props: true,
			beforeEnter(to) {
				const store = useInsightsStore();
				// Refresh is async, but we'll let the view load while the data is being fetched
				store.refresh(to.params.primaryKey as string);
			},
			children: [
				{
					name: 'panel-detail',
					path: ':panelKey',
					props: true,
					components: {
						detail: InsightsPanelConfiguration,
					},
				},
			],
		},
	],
	preRegisterCheck(user, permissions) {
		const admin = user.admin_access;

		if (admin) return true;

		const access = permissions['clairview_dashboards']?.['read']?.access;
		return access === 'partial' || access === 'full';
	},
});
