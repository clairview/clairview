import type { MergeCoreCollection } from '../index.js';
import type { ClairviewFolder } from './folder.js';
import type { ClairviewUser } from './user.js';

// Base type for clairview_files
export type ClairviewFile<Schema = any> = MergeCoreCollection<
	Schema,
	'clairview_files',
	{
		id: string;
		storage: string;
		filename_disk: string | null;
		filename_download: string;
		title: string | null;
		type: string | null;
		folder: ClairviewFolder<Schema> | string | null;
		uploaded_by: ClairviewUser<Schema> | string | null;
		uploaded_on: 'datetime';
		modified_by: ClairviewUser<Schema> | string | null;
		modified_on: 'datetime';
		charset: string | null;
		filesize: string | null;
		width: number | null;
		height: number | null;
		duration: number | null;
		embed: unknown | null;
		description: string | null;
		location: string | null;
		tags: string[] | null;
		metadata: Record<string, any> | null;
		focal_point_x: number | null;
		focal_point_y: number | null;
	}
>;
