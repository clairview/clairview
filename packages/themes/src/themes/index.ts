import type { Theme } from '../schemas/index.js';
import { clairviewDefault as darkClairviewDefault } from './dark/index.js';
import {
	clairviewColorMatch as lightClairviewColorMatch,
	clairviewDefault as lightClairviewDefault,
	clairviewMinimal as lightClairviewMinimal,
} from './light/index.js';

// We're using manually defined arrays here to guarantee the order
export const dark: Theme[] = [darkClairviewDefault];
export const light: Theme[] = [lightClairviewDefault, lightClairviewMinimal, lightClairviewColorMatch];
