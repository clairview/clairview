import type { ExtensionType } from '@clairview/extensions';

export interface ListQuery {
	type?: ExtensionType;
	search?: string;
	limit?: number;
	offset?: number;
	by?: string;
	sort?: 'popular' | 'recent' | 'downloads';
	sandbox?: boolean;
}
