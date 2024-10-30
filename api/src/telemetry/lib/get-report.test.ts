import { useEnv } from '@clairview/env';
import { version } from 'clairview/version';
import { type Knex } from 'knex';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import { getDatabase, getDatabaseClient } from '../../database/index.js';
import { fetchUserCount, type UserCount } from '../../utils/fetch-user-count/fetch-user-count.js';
import { getExtensionCount, type ExtensionCount } from '../utils/get-extension-count.js';
import { getFieldCount, type FieldCount } from '../utils/get-field-count.js';
import { getFilesizeSum, type FilesizeSum } from '../utils/get-filesize-sum.js';
import { getItemCount } from '../utils/get-item-count.js';
import { getUserItemCount, type UserItemCount } from '../utils/get-user-item-count.js';
import { getReport } from './get-report.js';

vi.mock('../../database/index.js');

vi.mock('../../database/helpers/index.js', () => ({
	getHelpers: vi.fn().mockImplementation(() => ({
		schema: {
			getDatabaseSize: vi.fn().mockReturnValue(0),
		},
	})),
}));

// This is required because logger uses global env which is imported before the tests run. Can be
// reduce to just mock the file when logger is also using useLogger everywhere @TODO
vi.mock('@clairview/env', () => ({
	useEnv: vi.fn().mockReturnValue({
		EMAIL_TEMPLATES_PATH: './templates',
	}),
}));

vi.mock('../utils/get-item-count.js');
vi.mock('../utils/get-storage.js');
vi.mock('../utils/get-user-item-count.js');
vi.mock('../utils/get-field-count.js');
vi.mock('../utils/get-extension-count.js');
vi.mock('../../utils/fetch-user-count/fetch-user-count.js');
vi.mock('../utils/get-filesize-sum.js');

let mockEnv: Record<string, unknown>;
let mockDb: Knex;
let mockUserCounts: UserCount;
let mockUserItemCounts: UserItemCount;
let mockFieldCounts: FieldCount;
let mockExtensionCounts: ExtensionCount;
let mockFilesizeSums: FilesizeSum;

beforeEach(() => {
	mockEnv = {
		PUBLIC_URL: 'test-public-url',
	};

	mockDb = {} as unknown as Knex;

	mockUserCounts = { admin: 5, app: 3, api: 15 };

	mockUserItemCounts = { collections: 25, items: 15000 };

	mockFieldCounts = { max: 28, total: 88 };

	mockExtensionCounts = { totalEnabled: 55 };

	mockFilesizeSums = { total: 10 };

	vi.mocked(useEnv).mockReturnValue(mockEnv);
	vi.mocked(getDatabase).mockReturnValue(mockDb);

	vi.mocked(getItemCount).mockResolvedValue({});
	vi.mocked(fetchUserCount).mockResolvedValue(mockUserCounts);
	vi.mocked(getUserItemCount).mockResolvedValue(mockUserItemCounts);
	vi.mocked(getFieldCount).mockResolvedValue(mockFieldCounts);
	vi.mocked(getExtensionCount).mockResolvedValue(mockExtensionCounts);
	vi.mocked(getFilesizeSum).mockResolvedValue(mockFilesizeSums);
});

afterEach(() => {
	vi.clearAllMocks();
});

test('Returns environment information', async () => {
	vi.mocked(getDatabaseClient).mockReturnValue('test-db' as any);

	const report = await getReport();

	expect(report.url).toBe(mockEnv['PUBLIC_URL']);
	expect(report.database).toBe('test-db');
	expect(report.version).toBe(version);
});

test('Runs and returns basic counts', async () => {
	const mockItemCount = {
		clairview_dashboards: 15,
		clairview_files: 45,
		clairview_flows: 60,
		clairview_roles: 75,
		clairview_shares: 90,
	};

	vi.mocked(getItemCount).mockResolvedValue(mockItemCount);

	const report = await getReport();

	expect(getItemCount).toHaveBeenCalledWith(mockDb, [
		{ collection: 'clairview_dashboards' },
		{ collection: 'clairview_files' },
		{ collection: 'clairview_flows', where: ['status', '=', 'active'] },
		{ collection: 'clairview_roles' },
		{ collection: 'clairview_shares' },
	]);

	expect(report.dashboards).toBe(mockItemCount.clairview_dashboards);
	expect(report.files).toBe(mockItemCount.clairview_files);
	expect(report.flows).toBe(mockItemCount.clairview_flows);
	expect(report.roles).toBe(mockItemCount.clairview_roles);
	expect(report.shares).toBe(mockItemCount.clairview_shares);
});

test('Runs and returns user counts', async () => {
	const report = await getReport();

	expect(fetchUserCount).toHaveBeenCalledWith({ knex: mockDb });

	expect(report.admin_users).toBe(mockUserCounts.admin);
	expect(report.app_users).toBe(mockUserCounts.app);
	expect(report.api_users).toBe(mockUserCounts.api);
});

test('Runs and returns user item counts', async () => {
	const report = await getReport();

	expect(getUserItemCount).toHaveBeenCalledWith(mockDb);

	expect(report.collections).toBe(mockUserItemCounts.collections);
	expect(report.items).toBe(mockUserItemCounts.items);
});

test('Runs and returns field counts', async () => {
	const report = await getReport();

	expect(getFieldCount).toHaveBeenCalledWith(mockDb);

	expect(report.fields_max).toBe(mockFieldCounts.max);
	expect(report.fields_total).toBe(mockFieldCounts.total);
});

test('Runs and returns extension counts', async () => {
	const report = await getReport();

	expect(getExtensionCount).toHaveBeenCalledWith(mockDb);

	expect(report.extensions).toBe(mockExtensionCounts.totalEnabled);
});

test('Runs and returns extension counts', async () => {
	const report = await getReport();

	expect(getFilesizeSum).toHaveBeenCalledWith(mockDb);

	expect(report.files_size_total).toBe(mockFilesizeSums.total);
});
