import jwt from 'jsonwebtoken';
import { InvalidTokenError, ServiceUnavailableError, TokenExpiredError } from '@clairview/errors';
import type { ClairviewTokenPayload } from '../types/index.js';

export function verifyJWT(token: string, secret: string) {
	let payload;

	try {
		payload = jwt.verify(token, secret, {
			issuer: 'clairview',
		}) as Record<string, unknown>;
	} catch (err) {
		if (err instanceof jwt.TokenExpiredError) {
			throw new TokenExpiredError();
		} else if (err instanceof jwt.JsonWebTokenError) {
			throw new InvalidTokenError();
		} else {
			throw new ServiceUnavailableError({ service: 'jwt', reason: `Couldn't verify token.` });
		}
	}

	return payload;
}

export function verifyAccessJWT(token: string, secret: string) {
	const payload = verifyJWT(token, secret) as ClairviewTokenPayload;

	if (payload.role === undefined || payload.app_access === undefined || payload.admin_access === undefined) {
		throw new InvalidTokenError();
	}

	return payload;
}
