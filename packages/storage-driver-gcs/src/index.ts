import type { Driver, ReadOptions } from '@clairview/storage';
import { normalizePath } from '@clairview/utils';
import type { Bucket, CreateReadStreamOptions, GetFilesOptions } from '@google-cloud/storage';
import { Storage } from '@google-cloud/storage';
import { join } from 'node:path';
import type { Readable } from 'node:stream';
import { pipeline } from 'node:stream/promises';

export type DriverGCSConfig = {
	root?: string;
	bucket: string;
	apiEndpoint?: string;
};

export class DriverGCS implements Driver {
	private root: string;
	private bucket: Bucket;

	constructor(config: DriverGCSConfig) {
		const { bucket, root, ...storageOptions } = config;

		this.root = root ? normalizePath(root, { removeLeading: true }) : '';

		const storage = new Storage(storageOptions);
		this.bucket = storage.bucket(bucket);
	}

	private fullPath(filepath: string) {
		return normalizePath(join(this.root, filepath));
	}

	private file(filepath: string) {
		return this.bucket.file(filepath);
	}

	async read(filepath: string, options?: ReadOptions) {
		const { range } = options || {};

		const stream_options: CreateReadStreamOptions = {};

		if (range?.start) stream_options.start = range.start;
		if (range?.end) stream_options.end = range.end;

		return this.file(this.fullPath(filepath)).createReadStream(stream_options);
	}

	async write(filepath: string, content: Readable) {
		const file = this.file(this.fullPath(filepath));
		const stream = file.createWriteStream({ resumable: false });
		await pipeline(content, stream);
	}

	async delete(filepath: string) {
		await this.file(this.fullPath(filepath)).delete();
	}

	async stat(filepath: string) {
		const [{ size, updated }] = await this.file(this.fullPath(filepath)).getMetadata();
		return { size: size as number, modified: new Date(updated as string) };
	}

	async exists(filepath: string) {
		return (await this.file(this.fullPath(filepath)).exists())[0];
	}

	async move(src: string, dest: string) {
		await this.file(this.fullPath(src)).move(this.file(this.fullPath(dest)));
	}

	async copy(src: string, dest: string) {
		await this.file(this.fullPath(src)).copy(this.file(this.fullPath(dest)));
	}

	async *list(prefix = '') {
		let query: GetFilesOptions = {
			prefix: this.fullPath(prefix),
			autoPaginate: false,
			maxResults: 500,
		};

		while (query) {
			const [files, nextQuery] = await this.bucket.getFiles(query);

			for (const file of files) {
				yield file.name.substring(this.root.length);
			}

			query = nextQuery;
		}
	}
}

export default DriverGCS;
