import type { Filter } from '@clairview/types';
import { validatePayload } from '@clairview/utils';
import { defineOperationApi } from '@clairview/extensions';

type Options = {
	filter: Filter;
};

export default defineOperationApi<Options>({
	id: 'condition',

	handler: ({ filter }, { data }) => {
		const errors = validatePayload(filter, data, { requireAll: true });

		if (errors.length > 0) {
			throw errors;
		} else {
			return null;
		}
	},
});
