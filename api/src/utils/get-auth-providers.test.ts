import { useEnv } from '@clairview/env';
import { describe, expect, test, vi } from 'vitest';
import { getAuthProviders } from './get-auth-providers.js';

vi.mock('@clairview/env');

const scenarios = [
	{
		name: 'when no providers configured',
		input: {},
		output: [],
	},
	{
		name: 'when no driver configured',
		input: {
			AUTH_PROVIDERS: 'clairview',
		},
		output: [],
	},

	{
		name: 'when single provider and driver are properly configured',
		input: {
			AUTH_PROVIDERS: 'clairview',
			AUTH_CLAIRVIEW_DRIVER: 'openid',
			AUTH_CLAIRVIEW_LABEL: 'Clairview',
			AUTH_CLAIRVIEW_ICON: 'hare',
		},
		output: [
			{
				name: 'clairview',
				driver: 'openid',
				label: 'Clairview',
				icon: 'hare',
			},
		],
	},

	{
		name: 'when multiple provider and driver are properly configured',
		input: {
			AUTH_PROVIDERS: 'clairview,custom',
			AUTH_CLAIRVIEW_DRIVER: 'openid',
			AUTH_CLAIRVIEW_LABEL: 'Clairview',
			AUTH_CLAIRVIEW_ICON: 'hare',
			AUTH_CUSTOM_DRIVER: 'openid',
			AUTH_CUSTOM_ICON: 'lock',
		},
		output: [
			{
				name: 'clairview',
				driver: 'openid',
				label: 'Clairview',
				icon: 'hare',
			},
			{
				name: 'custom',
				driver: 'openid',
				icon: 'lock',
			},
		],
	},
];

describe('get auth providers', () => {
	for (const scenario of scenarios) {
		test(scenario.name, () => {
			vi.mocked(useEnv).mockReturnValue(scenario.input);

			expect(getAuthProviders()).toEqual(scenario.output);
		});
	}
});
