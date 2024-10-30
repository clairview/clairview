import type { Driver } from '@clairview/storage';

export const _aliasMap: Record<string, string> = {
	local: '@clairview/storage-driver-local',
	s3: '@clairview/storage-driver-s3',
	supabase: '@clairview/storage-driver-supabase',
	gcs: '@clairview/storage-driver-gcs',
	azure: '@clairview/storage-driver-azure',
	cloudinary: '@clairview/storage-driver-cloudinary',
};

export const getStorageDriver = async (driverName: string): Promise<typeof Driver> => {
	if (driverName in _aliasMap) {
		driverName = _aliasMap[driverName]!;
	} else {
		throw new Error(`Driver "${driverName}" doesn't exist.`);
	}

	return (await import(driverName)).default;
};
