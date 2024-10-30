import type { Config } from './types';

const config: Config = {
	repo: 'clairview/clairview',
	mainPackage: 'clairview',
	typedTitles: {
		major: '⚠️ Potential Breaking Changes',
		minor: '✨ New Features & Improvements',
		patch: '🐛 Bug Fixes & Optimizations',
		none: '📎 Misc.',
	},
	untypedPackageTitles: {
		docs: '📝 Documentation',
		'tests-blackbox': '🧪 Blackbox Tests',
	},
	versionTitle: '📦 Published Versions',
	noticeType: 'major',
	// '@clairview/app' should always be listed before '@clairview/api', other packages don't matter
	packageOrder: ['@clairview/app', '@clairview/api'],
	linkedPackages: [
		// Ensure '@clairview/app' is bumped with 'clairview' to reflect correct main version in app
		['clairview', '@clairview/app'],
	],
};

export default config;
