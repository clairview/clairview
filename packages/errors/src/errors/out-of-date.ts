import { createError, ErrorCode } from '../index.js';

export const OutOfDateError = createError(
	ErrorCode.OutOfDate,
	'Operation could not be executed: Your current instance of Clairview is out of date.',
	503,
);
