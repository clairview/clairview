import { expect, test, vi } from 'vitest';
import { isClairviewVariable } from './is-clairview-variable.js';

vi.mock('../constants/clairview-variables.js', () => ({
	CLAIRVIEW_VARIABLES_REGEX: [/TEST_.*/],
}));

test('Returns false if variable matches none of the regexes', () => {
	expect(isClairviewVariable('NO')).toBe(false);
});

test('Returns true if variable matches one or more of the regexes', () => {
	expect(isClairviewVariable('TEST_123')).toBe(true);
});

test('Checks against original name if variable is suffixed with _FILE', () => {
	expect(isClairviewVariable('NO_FILE')).toBe(false);
	expect(isClairviewVariable('TEST_123_FILE')).toBe(true);
});
