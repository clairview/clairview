import { createClairview, rest } from '@clairview/sdk';
import type { Schema } from '../types/schema.js';

export const client = createClairview<Schema>('https://marketing.clairview.app').with(rest());
