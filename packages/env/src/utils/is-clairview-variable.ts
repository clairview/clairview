import { CLAIRVIEW_VARIABLES_REGEX } from '../constants/clairview-variables.js';

export const isClairviewVariable = (key: string): boolean => {
	if (key.endsWith('_FILE')) {
		key = key.slice(0, -5);
	}

	return CLAIRVIEW_VARIABLES_REGEX.some((regex) => regex.test(key));
};
