import { createError } from '@clairview/errors';
import type { GraphQLError } from 'graphql';

interface GraphQLValidationErrorExtensions {
	errors: GraphQLError[];
}

export const GraphQLValidationError = createError<GraphQLValidationErrorExtensions>(
	'GRAPHQL_VALIDATION',
	'GraphQL validation error.',
	400,
);
