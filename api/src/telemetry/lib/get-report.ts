import { useEnv } from '@clairview/env';
import { version } from 'clairview/version';
import { getHelpers } from '../../database/helpers/index.js';
import { getDatabase, getDatabaseClient } from '../../database/index.js';
import { fetchUserCount } from '../../utils/fetch-user-count/fetch-user-count.js';
import type { TelemetryReport } from '../types/report.js';
import { getExtensionCount } from '../utils/get-extension-count.js';
import { getFieldCount } from '../utils/get-field-count.js';
import { getFilesizeSum } from '../utils/get-filesize-sum.js';
import { getItemCount } from '../utils/get-item-count.js';
import { getUserItemCount } from '../utils/get-user-item-count.js';

const basicCountTasks = [
	{ collection: 'clairview_dashboards' },
	{ collection: 'clairview_files' },
	{
		collection: 'clairview_flows',
		where: ['status', '=', 'active'],
	},
	{ collection: 'clairview_roles' },
	{ collection: 'clairview_shares' },
] as const;

/**
 * Create a telemetry report about the anonymous usage of the current installation
 */
export const getReport = async (): Promise<TelemetryReport> => {
	const db = getDatabase();
	const env = useEnv();
	const helpers = getHelpers(db);

	const [basicCounts, userCounts, userItemCount, fieldsCounts, extensionsCounts, databaseSize, filesizes] =
		await Promise.all([
			getItemCount(db, basicCountTasks),
			fetchUserCount({ knex: db }),
			getUserItemCount(db),
			getFieldCount(db),
			getExtensionCount(db),
			helpers.schema.getDatabaseSize(),
			getFilesizeSum(db),
		]);

	return {
		url: env['PUBLIC_URL'] as string,
		version: version,
		database: getDatabaseClient(),

		dashboards: basicCounts.clairview_dashboards,
		files: basicCounts.clairview_files,
		flows: basicCounts.clairview_flows,
		roles: basicCounts.clairview_roles,
		shares: basicCounts.clairview_shares,

		admin_users: userCounts.admin,
		app_users: userCounts.app,
		api_users: userCounts.api,

		collections: userItemCount.collections,
		items: userItemCount.items,

		fields_max: fieldsCounts.max,
		fields_total: fieldsCounts.total,

		extensions: extensionsCounts.totalEnabled,

		database_size: databaseSize ?? 0,
		files_size_total: filesizes.total,
	};
};
