#!/usr/bin/env node
import { updateCheck } from '@clairview/update-check';
import { version } from './version.js';

if (version) {
	await updateCheck(version);
}

import('@clairview/api/cli/run.js');
