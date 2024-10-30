import { expectTypeOf, test } from 'vitest';
import { ErrorCode } from './codes.js';
import { type ClairviewError } from './create-error.js';
import { ContainsNullValuesError, type ContainsNullValuesErrorExtensions } from './errors/contains-null-values.js';
import { ContentTooLargeError } from './errors/content-too-large.js';
import { isClairviewError } from './is-clairview-error.js';

test('Guards input as ClairviewError', () => {
	expectTypeOf(isClairviewError).guards.toEqualTypeOf<ClairviewError<unknown>>();
});

test('Returns specific type when provided code for built-in error', () => {
	const contentTooLargeError = new ContentTooLargeError();

	if (isClairviewError(contentTooLargeError, ErrorCode.ContentTooLarge)) {
		expectTypeOf(contentTooLargeError).toEqualTypeOf<ClairviewError<never>>();
	}

	const containsNullValuesError = new ContainsNullValuesError({ collection: 'sample', field: 'sample' });

	if (isClairviewError(containsNullValuesError, ErrorCode.ContainsNullValues)) {
		expectTypeOf(containsNullValuesError).toEqualTypeOf<ClairviewError<ContainsNullValuesErrorExtensions>>();
	}
});

test('Returns unknown when provided code is not a built-in error', () => {
	const error = { name: 'ClairviewError', code: 'CustomError' };

	if (isClairviewError(error, error.code)) {
		expectTypeOf(error).toEqualTypeOf<ClairviewError<unknown>>();
	}
});

test('Allows to pass custom extensions type', () => {
	const error = { name: 'ClairviewError' };

	type CustomClairviewErrorExtensions = { custom: string };

	if (isClairviewError<CustomClairviewErrorExtensions>(error)) {
		expectTypeOf(error).toEqualTypeOf<ClairviewError<CustomClairviewErrorExtensions>>();
	}
});
