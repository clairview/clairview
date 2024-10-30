import type { EndpointConfig, HookConfig, OperationApiConfig } from '@clairview/extensions';

export type BundleConfig = {
	endpoints: { name: string; config: EndpointConfig }[];
	hooks: { name: string; config: HookConfig }[];
	operations: { name: string; config: OperationApiConfig }[];
};

export interface ExtensionManagerOptions {
	schedule: boolean;
	watch: boolean;
}
