import type { ClairviewError } from './create-error.js';
import type { ExtensionsMap } from './types.js';

/**
 * Check whether or not a passed value is a valid Clairview error.
 *
 * @param value - Any value
 * @param code - Error code to check for
 */
export const isClairviewError = <T = never, C extends string = string>(
	value: unknown,
	code?: C,
): value is ClairviewError<[T] extends [never] ? (C extends keyof ExtensionsMap ? ExtensionsMap[C] : unknown) : T> => {
	const isClairviewError =
		typeof value === 'object' &&
		value !== null &&
		Array.isArray(value) === false &&
		'name' in value &&
		value.name === 'ClairviewError';

	if (code) {
		return isClairviewError && 'code' in value && value.code === code.toUpperCase();
	}

	return isClairviewError;
};
