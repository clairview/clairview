import type { JsonValue } from '@clairview/types';

export default function tryParseJson(str: string): JsonValue | undefined {
	try {
		return JSON.parse(str);
	} catch {
		return undefined;
	}
}
