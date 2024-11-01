import { vi, expect, test, afterEach } from 'vitest';
import { useEnv } from '@clairview/env';
import { isLoginRedirectAllowed } from './is-login-redirect-allowed.js';

vi.mock('@clairview/env');

afterEach(() => {
	vi.clearAllMocks();
});

test('isLoginRedirectAllowed returns true with no redirect', () => {
	const redirect = undefined;
	const provider = 'local';

	expect(isLoginRedirectAllowed(redirect, provider)).toBe(true);
});

test('isLoginRedirectAllowed returns false with invalid redirect', () => {
	const redirect = 123456;
	const provider = 'local';

	expect(isLoginRedirectAllowed(redirect, provider)).toBe(false);
});

test('isLoginRedirectAllowed returns true for allowed URL', () => {
	const provider = 'local';

	vi.mocked(useEnv).mockReturnValue({
		[`AUTH_${provider.toUpperCase()}_REDIRECT_ALLOW_LIST`]:
			'http://external.example.com,https://external.example.com,http://external.example.com:8055/test',
		PUBLIC_URL: 'http://public.example.com',
	});

	expect(isLoginRedirectAllowed('http://public.example.com', provider)).toBe(true);
	expect(isLoginRedirectAllowed('http://external.example.com', provider)).toBe(true);
	expect(isLoginRedirectAllowed('https://external.example.com', provider)).toBe(true);
	expect(isLoginRedirectAllowed('http://external.example.com:8055/test', provider)).toBe(true);
});

test('isLoginRedirectAllowed returns false for denied URL', () => {
	const provider = 'local';

	vi.mocked(useEnv).mockReturnValue({
		[`AUTH_${provider.toUpperCase()}_REDIRECT_ALLOW_LIST`]: 'http://external.example.com',
		PUBLIC_URL: 'http://public.example.com',
	});

	expect(isLoginRedirectAllowed('https://external.example.com', provider)).toBe(false);
	expect(isLoginRedirectAllowed('http://external.example.com:8055', provider)).toBe(false);
	expect(isLoginRedirectAllowed('http://external.example.com/test', provider)).toBe(false);
});

test('isLoginRedirectAllowed returns true for relative paths', () => {
	const provider = 'local';

	vi.mocked(useEnv).mockReturnValue({
		[`AUTH_${provider.toUpperCase()}_REDIRECT_ALLOW_LIST`]: 'http://external.example.com',
		PUBLIC_URL: 'http://public.example.com',
	});

	expect(isLoginRedirectAllowed('/admin/content', provider)).toBe(true);
	expect(isLoginRedirectAllowed('../admin/content', provider)).toBe(true);
	expect(isLoginRedirectAllowed('./admin/content', provider)).toBe(true);

	expect(isLoginRedirectAllowed('http://public.example.com/admin/content', provider)).toBe(true);
});

test('isLoginRedirectAllowed returns false if missing protocol', () => {
	const provider = 'local';

	vi.mocked(useEnv).mockReturnValue({
		[`AUTH_${provider.toUpperCase()}_REDIRECT_ALLOW_LIST`]: 'http://example.com',
		PUBLIC_URL: 'http://example.com',
	});

	expect(isLoginRedirectAllowed('//example.com/admin/content', provider)).toBe(false);
	expect(isLoginRedirectAllowed('//user@password:example.com/', provider)).toBe(false);
});
