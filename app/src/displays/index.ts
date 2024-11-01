import type { DisplayConfig } from '@clairview/extensions';
import { sortBy } from 'lodash';
import { App } from 'vue';

export function getInternalDisplays(): DisplayConfig[] {
	const displays = import.meta.glob<DisplayConfig>('./*/index.ts', { import: 'default', eager: true });

	return sortBy(Object.values(displays), 'id');
}

export function registerDisplays(displays: DisplayConfig[], app: App): void {
	for (const display of displays) {
		app.component(`display-${display.id}`, display.component);

		if (typeof display.options !== 'function' && Array.isArray(display.options) === false && display.options !== null) {
			app.component(`display-options-${display.id}`, display.options);
		}
	}
}
