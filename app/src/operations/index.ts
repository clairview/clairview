import type { OperationAppConfig } from '@clairview/extensions';
import { sortBy } from 'lodash';
import { App } from 'vue';

export function getInternalOperations(): OperationAppConfig[] {
	const operations = import.meta.glob<OperationAppConfig>('./*/index.ts', { import: 'default', eager: true });

	return sortBy(Object.values(operations), 'id');
}

export function registerOperations(operations: OperationAppConfig[], app: App): void {
	for (const operation of operations) {
		if (
			typeof operation.overview !== 'function' &&
			Array.isArray(operation.overview) === false &&
			operation.overview !== null
		) {
			app.component(`operation-overview-${operation.id}`, operation.overview);
		}

		if (
			typeof operation.options !== 'function' &&
			Array.isArray(operation.options) === false &&
			operation.options !== null
		) {
			app.component(`operation-options-${operation.id}`, operation.options);
		}
	}
}
