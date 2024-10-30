import jwt from 'jsonwebtoken';

/**
 * Check if a given string conforms to the structure of a JWT
 * and whether it is issued by Clairview.
 */
export default function isClairviewJWT(string: string): boolean {
	try {
		const payload = jwt.decode(string, { json: true });
		if (payload?.iss !== 'clairview') return false;
		return true;
	} catch {
		return false;
	}
}
