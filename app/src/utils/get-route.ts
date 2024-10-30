import { isSystemCollection } from '@clairview/system-data';

const accessibleSystemCollections = {
	clairview_users: { route: '/users' },
	clairview_files: { route: '/files' },
	clairview_dashboards: { route: '/insights' },
	clairview_activity: { route: '/activity' },
	clairview_settings: { route: '/settings/project', singleton: true },
	clairview_collections: { route: '/settings/data-model' },
	clairview_roles: { route: '/settings/roles' },
	clairview_presets: { route: '/settings/presets' },
	clairview_translations: { route: '/settings/translations' },
	clairview_webhooks: { route: '/settings/webhooks' },
	clairview_flows: { route: '/settings/flows' },
} as const;

function isAccessibleSystemCollection(collection: string): collection is keyof typeof accessibleSystemCollections {
	return collection in accessibleSystemCollections;
}

/**
 * Get the route of an accessible system collection in the admin app for a given collection name
 *
 * @param collection - Collection name
 * @returns - URL route for the system collection, empty string if not an accessible system collection
 */
export function getSystemCollectionRoute(collection: string) {
	if (isAccessibleSystemCollection(collection)) return accessibleSystemCollections[collection].route;

	return '';
}

/**
 * Get the route of a collection in the admin app for a given collection name
 *
 * @param collection - Collection name
 * @returns - URL route for the collection
 */
export function getCollectionRoute(collection: string | null) {
	if (collection === null) return '';

	if (isSystemCollection(collection)) return getSystemCollectionRoute(collection);

	return `/content/${collection}`;
}

/**
 * Get the route of an item in the admin app for a given collection name and primary key
 *
 * @param collection - Collection name
 * @param primaryKey - Primary key of item
 * @returns - URL route for the item
 */
export function getItemRoute(collection: string | null, primaryKey: string | number) {
	if (collection === null) return '';

	const collectionRoute = getCollectionRoute(collection);

	if (collectionRoute === '') return '';

	if (isAccessibleSystemCollection(collection) && 'singleton' in accessibleSystemCollections[collection])
		return collectionRoute;

	const itemRoute = primaryKey === '+' ? primaryKey : encodeURIComponent(primaryKey);

	return `${collectionRoute}/${itemRoute}`;
}
