import { ForbiddenError } from '@clairview/errors';
import {
	AccessService,
	ActivityService,
	CommentsService,
	DashboardsService,
	FilesService,
	FlowsService,
	FoldersService,
	ItemsService,
	NotificationsService,
	OperationsService,
	PanelsService,
	PermissionsService,
	PoliciesService,
	PresetsService,
	RevisionsService,
	RolesService,
	SettingsService,
	SharesService,
	TranslationsService,
	UsersService,
	VersionsService,
	WebhooksService,
} from '../services/index.js';
import type { AbstractServiceOptions } from '../types/services.js';

/**
 * Select the correct service for the given collection. This allows the individual services to run
 * their custom checks (f.e. it allows `UsersService` to prevent updating TFA secret from outside).
 */
export function getService(collection: string, opts: AbstractServiceOptions): ItemsService {
	switch (collection) {
		case 'clairview_access':
			return new AccessService(opts);
		case 'clairview_activity':
			return new ActivityService(opts);
		case 'clairview_comments':
			return new CommentsService({ ...opts, serviceOrigin: 'comments' });
		case 'clairview_dashboards':
			return new DashboardsService(opts);
		case 'clairview_files':
			return new FilesService(opts);
		case 'clairview_flows':
			return new FlowsService(opts);
		case 'clairview_folders':
			return new FoldersService(opts);
		case 'clairview_notifications':
			return new NotificationsService(opts);
		case 'clairview_operations':
			return new OperationsService(opts);
		case 'clairview_panels':
			return new PanelsService(opts);
		case 'clairview_permissions':
			return new PermissionsService(opts);
		case 'clairview_presets':
			return new PresetsService(opts);
		case 'clairview_policies':
			return new PoliciesService(opts);
		case 'clairview_revisions':
			return new RevisionsService(opts);
		case 'clairview_roles':
			return new RolesService(opts);
		case 'clairview_settings':
			return new SettingsService(opts);
		case 'clairview_shares':
			return new SharesService(opts);
		case 'clairview_translations':
			return new TranslationsService(opts);
		case 'clairview_users':
			return new UsersService(opts);
		case 'clairview_versions':
			return new VersionsService(opts);
		case 'clairview_webhooks':
			return new WebhooksService(opts);
		default:
			// Deny usage of other system collections via ItemsService
			if (collection.startsWith('clairview_')) throw new ForbiddenError();

			return new ItemsService(collection, opts);
	}
}
