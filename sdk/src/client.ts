import type { ClientGlobals, ClientOptions, ClairviewClient } from './types/client.js';

/**
 * The default globals supplied to the client
 */
const defaultGlobals: ClientGlobals = {
	fetch: globalThis.fetch,
	WebSocket: globalThis.WebSocket,
	URL: globalThis.URL,
	logger: globalThis.console,
};

/**
 * Creates a client to communicate with a Clairview app.
 *
 * @param url The URL to the Clairview app.
 * @param config The optional configuration.
 *
 * @returns A Clairview client.
 */
export const createClairview = <Schema = any>(url: string, options: ClientOptions = {}): ClairviewClient<Schema> => {
	const globals = options.globals ? { ...defaultGlobals, ...options.globals } : defaultGlobals;
	return {
		globals,
		url: new globals.URL(url),
		with(createExtension) {
			return {
				...this,
				...createExtension(this),
			};
		},
	};
};
