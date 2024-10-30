import getDatabase from '../database/index.js';
import { InvalidCredentialsError } from '@clairview/errors';
import type { ClairviewTokenPayload } from '../types/index.js';

/**
 * Verifies the associated session is still available and valid.
 *
 * @throws If session not found.
 */
export async function verifySessionJWT(payload: ClairviewTokenPayload) {
	const database = getDatabase();

	const session = await database
		.select(1)
		.from('clairview_sessions')
		.where({
			token: payload['session'],
			user: payload['id'] || null,
			share: payload['share'] || null,
		})
		.andWhere('expires', '>=', new Date())
		.first();

	if (!session) {
		throw new InvalidCredentialsError();
	}
}
