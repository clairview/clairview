import { useEnv } from '@clairview/env';
import { ErrorCode, ForbiddenError, isClairviewError, RouteNotFoundError } from '@clairview/errors';
import { EXTENSION_TYPES } from '@clairview/extensions';
import {
	account,
	describe,
	list,
	type AccountOptions,
	type DescribeOptions,
	type ListOptions,
	type ListQuery,
} from '@clairview/extensions-registry';
import type { FieldFilter } from '@clairview/types';
import { isIn } from '@clairview/utils';
import express from 'express';
import { isNil } from 'lodash-es';
import { UUID_REGEX } from '../constants.js';
import { getExtensionManager } from '../extensions/index.js';
import { respond } from '../middleware/respond.js';
import useCollection from '../middleware/use-collection.js';
import { ExtensionReadError, ExtensionsService } from '../services/extensions.js';
import asyncHandler from '../utils/async-handler.js';
import { getCacheControlHeader } from '../utils/get-cache-headers.js';
import { getMilliseconds } from '../utils/get-milliseconds.js';

const router = express.Router();
const env = useEnv();

router.use(useCollection('clairview_extensions'));

router.get(
	'/',
	asyncHandler(async (req, res, next) => {
		const service = new ExtensionsService({
			accountability: req.accountability,
			schema: req.schema,
		});

		const extensions = await service.readAll();
		res.locals['payload'] = { data: extensions || null };
		return next();
	}),
	respond,
);

router.get(
	'/registry',
	asyncHandler(async (req, res, next) => {
		if (req.accountability && req.accountability.admin !== true) {
			throw new ForbiddenError();
		}

		const { search, limit, offset, sort, filter } = req.sanitizedQuery;

		const query: ListQuery = {};

		if (!isNil(search)) {
			query.search = search;
		}

		if (!isNil(limit)) {
			query.limit = limit;
		}

		if (!isNil(offset)) {
			query.offset = offset;
		}

		if (filter) {
			const getFilterValue = (key: string) => {
				const field = (filter as FieldFilter)[key];
				if (!field || !('_eq' in field) || typeof field._eq !== 'string') return;
				return field._eq;
			};

			const by = getFilterValue('by');
			const type = getFilterValue('type');

			if (by) {
				query.by = by;
			}

			if (type) {
				if (isIn(type, EXTENSION_TYPES) === false) {
					throw new ForbiddenError();
				}

				query.type = type;
			}
		}

		if (!isNil(sort) && sort[0] && isIn(sort[0], ['popular', 'recent', 'downloads'] as const)) {
			query.sort = sort[0];
		}

		if (env['MARKETPLACE_TRUST'] === 'sandbox') {
			query.sandbox = true;
		}

		const options: ListOptions = {};

		if (env['MARKETPLACE_REGISTRY'] && typeof env['MARKETPLACE_REGISTRY'] === 'string') {
			options.registry = env['MARKETPLACE_REGISTRY'];
		}

		const payload = await list(query, options);

		res.locals['payload'] = payload;
		return next();
	}),
	respond,
);

router.get(
	`/registry/account/:pk(${UUID_REGEX})`,
	asyncHandler(async (req, res, next) => {
		if (typeof req.params['pk'] !== 'string') {
			throw new ForbiddenError();
		}

		const options: AccountOptions = {};

		if (env['MARKETPLACE_REGISTRY'] && typeof env['MARKETPLACE_REGISTRY'] === 'string') {
			options.registry = env['MARKETPLACE_REGISTRY'];
		}

		const payload = await account(req.params['pk'], options);

		res.locals['payload'] = payload;
		return next();
	}),
	respond,
);

router.get(
	`/registry/extension/:pk(${UUID_REGEX})`,
	asyncHandler(async (req, res, next) => {
		if (typeof req.params['pk'] !== 'string') {
			throw new ForbiddenError();
		}

		const options: DescribeOptions = {};

		if (env['MARKETPLACE_REGISTRY'] && typeof env['MARKETPLACE_REGISTRY'] === 'string') {
			options.registry = env['MARKETPLACE_REGISTRY'];
		}

		const payload = await describe(req.params['pk'], options);

		res.locals['payload'] = payload;
		return next();
	}),
	respond,
);

router.post(
	'/registry/install',
	asyncHandler(async (req, _res, next) => {
		if (req.accountability && req.accountability.admin !== true) {
			throw new ForbiddenError();
		}

		const { version, extension } = req.body;

		if (!version || !extension) {
			throw new ForbiddenError();
		}

		const service = new ExtensionsService({
			accountability: req.accountability,
			schema: req.schema,
		});

		await service.install(extension, version);
		return next();
	}),
	respond,
);

router.post(
	'/registry/reinstall',
	asyncHandler(async (req, _res, next) => {
		if (req.accountability && req.accountability.admin !== true) {
			throw new ForbiddenError();
		}

		const { extension } = req.body;

		if (!extension) {
			throw new ForbiddenError();
		}

		const service = new ExtensionsService({
			accountability: req.accountability,
			schema: req.schema,
		});

		await service.reinstall(extension);
		return next();
	}),
	respond,
);

router.delete(
	`/registry/uninstall/:pk(${UUID_REGEX})`,
	asyncHandler(async (req, _res, next) => {
		if (req.accountability && req.accountability.admin !== true) {
			throw new ForbiddenError();
		}

		const pk = req.params['pk'];

		if (typeof pk !== 'string') {
			throw new ForbiddenError();
		}

		const service = new ExtensionsService({
			accountability: req.accountability,
			schema: req.schema,
		});

		await service.uninstall(pk);
		return next();
	}),
	respond,
);

router.patch(
	`/:pk(${UUID_REGEX})`,
	asyncHandler(async (req, res, next) => {
		if (req.accountability && req.accountability.admin !== true) {
			throw new ForbiddenError();
		}

		if (typeof req.params['pk'] !== 'string') {
			throw new ForbiddenError();
		}

		const service = new ExtensionsService({
			accountability: req.accountability,
			schema: req.schema,
		});

		try {
			const result = await service.updateOne(req.params['pk'], req.body);
			res.locals['payload'] = { data: result || null };
		} catch (error) {
			let finalError = error;

			if (error instanceof ExtensionReadError) {
				finalError = error.originalError;

				if (isClairviewError(finalError, ErrorCode.Forbidden)) {
					return next();
				}
			}

			throw finalError;
		}

		return next();
	}),
	respond,
);

router.delete(
	`/:pk(${UUID_REGEX})`,
	asyncHandler(async (req, _res, next) => {
		if (req.accountability && req.accountability.admin !== true) {
			throw new ForbiddenError();
		}

		const service = new ExtensionsService({
			accountability: req.accountability,
			schema: req.schema,
		});

		const pk = req.params['pk'];

		if (typeof pk !== 'string') {
			throw new ForbiddenError();
		}

		await service.deleteOne(pk);

		return next();
	}),
	respond,
);

router.get(
	'/sources/:chunk',
	asyncHandler(async (req, res) => {
		const chunk = req.params['chunk'] as string;
		const extensionManager = getExtensionManager();

		let source: string | null;

		if (chunk === 'index.js') {
			source = extensionManager.getAppExtensionsBundle();
		} else {
			source = extensionManager.getAppExtensionChunk(chunk);
		}

		if (source === null) {
			throw new RouteNotFoundError({ path: req.path });
		}

		res.setHeader('Content-Type', 'application/javascript; charset=UTF-8');

		res.setHeader(
			'Cache-Control',
			getCacheControlHeader(req, getMilliseconds(env['EXTENSIONS_CACHE_TTL']), false, false),
		);

		res.setHeader('Vary', 'Origin, Cache-Control');
		res.end(source);
	}),
);

export default router;
