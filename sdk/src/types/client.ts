import type { ConsoleInterface, FetchInterface, UrlInterface, WebSocketConstructor } from './globals.js';

/**
 * empty clairview client
 */
export interface ClairviewClient<Schema> {
	url: URL;
	globals: ClientGlobals;
	with: <Extension extends object>(createExtension: (client: ClairviewClient<Schema>) => Extension) => this & Extension;
}

/**
 * All used globals for the client
 */
export type ClientGlobals = {
	fetch: FetchInterface;
	WebSocket: WebSocketConstructor;
	URL: UrlInterface;
	logger: ConsoleInterface;
};

/**
 * Available options on the client
 */
export type ClientOptions = {
	globals?: Partial<ClientGlobals>;
};
