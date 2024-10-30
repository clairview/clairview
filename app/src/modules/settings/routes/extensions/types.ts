import { ExtensionType as ExtensionTypeOriginal } from '@clairview/extensions';

export type ExtensionState = 'enabled' | 'disabled' | 'partial';

export type ExtensionType = ExtensionTypeOriginal | 'missing';
