import { randomAlpha, randomInteger, randomIdentifier } from '@clairview/random';
import { beforeEach, expect, test } from 'vitest';
import { createError } from './create-error.js';
import { isClairviewError } from './is-clairview-error.js';

let sample: {
	code: string;
	status: number;
	message: string;
};

beforeEach(() => {
	sample = {
		code: randomAlpha(randomInteger(5, 25)),
		status: randomInteger(200, 599),
		message: randomAlpha(randomInteger(10, 50)),
	};
});

test('Reports false for non Clairview-errors', () => {
	const negative = [
		false,
		() => {
			/* empty */
		},
		[],
		new Error(),
		0,
		null,
		undefined,
		new Set(),
	];

	for (const input of negative) {
		expect(isClairviewError(input)).toBe(false);
	}
});

test('Reports true for Clairview error', () => {
	const SampleError = createError(sample.code, sample.message, sample.status);
	const error = new SampleError();
	expect(isClairviewError(error)).toBe(true);
});

test('Check against optional error code', () => {
	const SampleError = createError(sample.code, sample.message, sample.status);
	const error = new SampleError();
	expect(isClairviewError(error, sample.code)).toBe(true);
	expect(isClairviewError(error, randomIdentifier())).toBe(false);
});
