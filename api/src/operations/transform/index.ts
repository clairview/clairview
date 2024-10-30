import { defineOperationApi } from '@clairview/extensions';
import { optionToObject } from '@clairview/utils';

type Options = {
	json: string | Record<string, any>;
};

export default defineOperationApi<Options>({
	id: 'transform',

	handler: ({ json }) => {
		return optionToObject(json);
	},
});
