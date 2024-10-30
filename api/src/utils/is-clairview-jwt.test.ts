import isClairviewJWT from './is-clairview-jwt.js';
import jwt from 'jsonwebtoken';
import { test, expect } from 'vitest';

test('Returns false for non JWT string', () => {
	const result = isClairviewJWT('test');
	expect(result).toBe(false);
});

test('Returns false for JWTs with text payload', () => {
	const token = jwt.sign('plaintext', 'secret');
	const result = isClairviewJWT(token);
	expect(result).toBe(false);
});

test(`Returns false if token issuer isn't "clairview"`, () => {
	const token = jwt.sign({ payload: 'content' }, 'secret', { issuer: 'rijk' });
	const result = isClairviewJWT(token);
	expect(result).toBe(false);
});

test(`Returns true if token is valid JWT and issuer is "clairview"`, () => {
	const token = jwt.sign({ payload: 'content' }, 'secret', { issuer: 'clairview' });
	const result = isClairviewJWT(token);
	expect(result).toBe(true);
});
