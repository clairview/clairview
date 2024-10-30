export interface ClairviewError<Extensions = void> extends Error {
	extensions: Extensions;
	code: string;
	status: number;
}

export interface ClairviewErrorConstructor<Extensions = void> {
	new (extensions: Extensions, options?: ErrorOptions): ClairviewError<Extensions>;
	readonly prototype: ClairviewError<Extensions>;
}

export const createError = <Extensions = void>(
	code: string,
	message: string | ((extensions: Extensions) => string),
	status = 500,
): ClairviewErrorConstructor<Extensions> => {
	return class extends Error implements ClairviewError<Extensions> {
		override name = 'ClairviewError';
		extensions: Extensions;
		code = code.toUpperCase();
		status = status;

		constructor(extensions: Extensions, options?: ErrorOptions) {
			const msg = typeof message === 'string' ? message : message(extensions as Extensions);

			super(msg, options);

			this.extensions = extensions;
		}

		override toString() {
			return `${this.name} [${this.code}]: ${this.message}`;
		}
	};
};
