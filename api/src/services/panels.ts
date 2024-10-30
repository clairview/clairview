import type { AbstractServiceOptions } from '../types/index.js';
import { ItemsService } from './items.js';

export class PanelsService extends ItemsService {
	constructor(options: AbstractServiceOptions) {
		super('clairview_panels', options);
	}
}
