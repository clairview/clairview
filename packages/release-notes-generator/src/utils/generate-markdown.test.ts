import { describe, expect, test } from 'vitest';
import config from '../config.js';
import type { Change, Notice, PackageVersion, Type, UntypedPackage } from '../types.js';
import { generateMarkdown } from './generate-markdown.js';

const change1: Change = {
	summary: "Made Clairview even more magical\nAnd here's some additional context",
	commit: 'abcd123',
	githubInfo: {
		user: 'clairview',
		pull: 1,
		links: {
			commit: '[`abcd123`](https://github.com/clairview/clairview/commit/abcd123)',
			pull: '[#1](https://github.com/clairview/clairview/pull/1)',
			user: '[@clairview](https://github.com/clairview)',
		},
	},
};

const change2: Change = {
	summary: 'Improved some things a little',
	commit: 'efgh456',
	githubInfo: {
		user: 'clairview',
		pull: 2,
		links: {
			commit: '[`efgh456`](https://github.com/clairview/clairview/commit/efgh456)',
			pull: '[#2](https://github.com/clairview/clairview/pull/2)',
			user: '[@clairview](https://github.com/clairview)',
		},
	},
};

test('should generate basic release notes', () => {
	const types: Type[] = [
		{
			title: config.typedTitles.minor,
			packages: [
				{
					name: '@clairview/api',
					changes: [change1],
				},
			],
		},
		{
			title: config.typedTitles.patch,
			packages: [
				{
					name: '@clairview/app',
					changes: [change1, change2],
				},
			],
		},
	];

	const untypedPackages: UntypedPackage[] = [
		{ name: config.untypedPackageTitles['docs']!, changes: [change1, change2] },
		{ name: config.untypedPackageTitles['tests-blackbox']!, changes: [change1] },
	];

	const packageVersions: PackageVersion[] = [
		{ name: '@clairview/api', version: '10.0.0' },
		{ name: '@clairview/app', version: '10.0.0' },
	];

	const markdown = generateMarkdown([], types, untypedPackages, packageVersions);

	expect(markdown).toMatchInlineSnapshot(`
		"### ✨ New Features & Improvements

		- **@clairview/api**
		  - Made Clairview even more magical ([#1](https://github.com/clairview/clairview/pull/1) by @clairview)
		    And here's some additional context

		### 🐛 Bug Fixes & Optimizations

		- **@clairview/app**
		  - Made Clairview even more magical ([#1](https://github.com/clairview/clairview/pull/1) by @clairview)
		    And here's some additional context
		  - Improved some things a little ([#2](https://github.com/clairview/clairview/pull/2) by @clairview)

		### 📝 Documentation

		- Made Clairview even more magical ([#1](https://github.com/clairview/clairview/pull/1) by @clairview)
		  And here's some additional context
		- Improved some things a little ([#2](https://github.com/clairview/clairview/pull/2) by @clairview)

		### 🧪 Blackbox Tests

		- Made Clairview even more magical ([#1](https://github.com/clairview/clairview/pull/1) by @clairview)
		  And here's some additional context

		### 📦 Published Versions

		- \`@clairview/api@10.0.0\`
		- \`@clairview/app@10.0.0\`"
	`);
});

describe('notices', () => {
	const notices: Notice[] = [
		{ notice: 'This is an example notice.', change: change1 },
		{ notice: 'This is another notice.', change: change2 },
	];

	test('should create section with notices when no changes', () => {
		const markdown = generateMarkdown(notices, [], [], []);

		expect(markdown).toMatchInlineSnapshot(`
			"### ⚠️ Potential Breaking Changes

			**Made Clairview even more magical... ([#1](https://github.com/clairview/clairview/pull/1))**
			This is an example notice.

			**Improved some things a little ([#2](https://github.com/clairview/clairview/pull/2))**
			This is another notice."
		`);
	});

	test('should show notices along with changes', () => {
		const types: Type[] = [
			{
				title: config.typedTitles[config.noticeType],
				packages: [
					{
						name: '@clairview/api',
						changes: [change1],
					},
				],
			},
		];

		const markdown = generateMarkdown(notices, types, [], []);

		expect(markdown).toMatchInlineSnapshot(`
			"### ⚠️ Potential Breaking Changes

			**Made Clairview even more magical... ([#1](https://github.com/clairview/clairview/pull/1))**
			This is an example notice.

			**Improved some things a little ([#2](https://github.com/clairview/clairview/pull/2))**
			This is another notice.

			- **@clairview/api**
			  - Made Clairview even more magical ([#1](https://github.com/clairview/clairview/pull/1) by @clairview)
			    And here's some additional context"
		`);
	});
});
