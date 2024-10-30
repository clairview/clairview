import { defineOperationApi } from '@clairview/extensions';
import { optionToString } from '@clairview/utils';
import { useLogger } from '../../logger/index.js';

type Options = {
	message: unknown;
};

export default defineOperationApi<Options>({
	id: 'log',

	handler: ({ message }) => {
		const logger = useLogger();

		logger.info(optionToString(message));
	},
});
