// @vitest-environment jsdom
import { expect, test } from 'vitest';
import { md } from './md.js';

test.each([
	{ value: 'test', expected: '<p>test</p>\n' },
	{
		value: `[Clairview](https://clairview.io)`,
		expected: '<p><a href="https://clairview.io" target="_self">Clairview</a></p>\n',
	},
	{
		value: `[Clairview](https://clairview.io)`,
		expected: '<p><a href="https://clairview.io" target="_blank" rel="noopener noreferrer">Clairview</a></p>\n',
		options: { target: '_blank' } as const,
	},
	{ value: `test<script>alert('alert')</script>`, expected: '<p>test</p>\n' },
])('should sanitize "$str" into "$expected"', ({ value, expected, options }) => {
	expect(md(value, options)).toBe(expected);
});
