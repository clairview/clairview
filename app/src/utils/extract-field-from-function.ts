import { REGEX_BETWEEN_PARENS } from '@clairview/constants';
import { FieldFunction } from '@clairview/types';

/**
 * Extracts the function and field name of a field wrapped in a function
 *
 * @param fieldKey - Field in function, for example `year(date_created)`
 * @return Object of function name and field key
 *
 * @example
 * ```js
 * extractFieldFromFunction('year(date_created)');
 * // => { fn: 'year', field: 'date_created' }
 * ```
 */
export function extractFieldFromFunction(fieldKey: string): { fn: FieldFunction | null; field: string } {
	let functionName;

	if (fieldKey.includes('(') && fieldKey.includes(')')) {
		functionName = fieldKey.split('(')[0] as FieldFunction | undefined;
		const match = fieldKey.match(REGEX_BETWEEN_PARENS);
		if (match) fieldKey = match[1] as string;
	}

	return { fn: functionName ?? null, field: fieldKey };
}
