import { InvalidCredentialsError } from '@clairview/errors';
import type { Accountability } from '@clairview/types';
import getDatabase from '../database/index.js';
import { fetchRolesTree } from '../permissions/lib/fetch-roles-tree.js';
import { fetchGlobalAccess } from '../permissions/modules/fetch-global-access/fetch-global-access.js';
import { createDefaultAccountability } from '../permissions/utils/create-default-accountability.js';
import { getSecret } from './get-secret.js';
import isClairviewJWT from './is-clairview-jwt.js';
import { verifyAccessJWT } from './jwt.js';
import { verifySessionJWT } from './verify-session-jwt.js';

export async function getAccountabilityForToken(
	token?: string | null,
	accountability?: Accountability,
): Promise<Accountability> {
	if (!accountability) {
		accountability = createDefaultAccountability();
	}

	// Try finding the user with the provided token
	const database = getDatabase();

	if (token) {
		if (isClairviewJWT(token)) {
			const payload = verifyAccessJWT(token, getSecret());

			if ('session' in payload) {
				await verifySessionJWT(payload);
			}

			if (payload.share) accountability.share = payload.share;
			if (payload.share_scope) accountability.share_scope = payload.share_scope;
			if (payload.id) accountability.user = payload.id;

			accountability.role = payload.role;
			accountability.roles = await fetchRolesTree(payload.role, database);

			const { admin, app } = await fetchGlobalAccess(accountability, database);

			accountability.admin = admin;
			accountability.app = app;
		} else {
			const user = await database
				.select('clairview_users.id', 'clairview_users.role')
				.from('clairview_users')
				.where({
					'clairview_users.token': token,
					status: 'active',
				})
				.first();

			if (!user) {
				throw new InvalidCredentialsError();
			}

			accountability.user = user.id;
			accountability.role = user.role;
			accountability.roles = await fetchRolesTree(user.role, database);

			const { admin, app } = await fetchGlobalAccess(accountability, database);

			accountability.admin = admin;
			accountability.app = app;
		}
	}

	return accountability;
}
