import { getAssetUrl } from '@/utils/get-asset-url';
import { cryptoStub } from '@/__utils__/crypto';
import { expect, test, vi } from 'vitest';
import { getPublicURL } from '@/utils/get-root-path';

vi.stubGlobal('crypto', cryptoStub);
vi.mock('@/utils/get-root-path');

test('Get asset url', () => {
	vi.mocked(getPublicURL).mockReturnValueOnce('https://clairview.io/');
	const output = getAssetUrl('test.jpg');
	expect(output).toBe(`https://clairview.io/assets/test.jpg`);
});

test('Get asset url for download', () => {
	vi.mocked(getPublicURL).mockReturnValueOnce('https://clairview.io/');
	const output = getAssetUrl('test.jpg', true);
	expect(output).toBe(`https://clairview.io/assets/test.jpg?download=`);
});

test('Subdirectory Install: Get asset url', () => {
	vi.mocked(getPublicURL).mockReturnValueOnce('https://clairview.io/subdirectory/');
	const output = getAssetUrl('test.jpg');
	expect(output).toBe(`https://clairview.io/subdirectory/assets/test.jpg`);
});

test('Subdirectory Install: Get asset url for download', () => {
	vi.mocked(getPublicURL).mockReturnValueOnce('https://clairview.io/subdirectory/');
	const output = getAssetUrl('test.jpg', true);
	expect(output).toBe(`https://clairview.io/subdirectory/assets/test.jpg?download=`);
});
