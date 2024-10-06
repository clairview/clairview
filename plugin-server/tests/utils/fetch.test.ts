import { FetchError } from 'node-fetch'

import { raiseIfUserProvidedUrlUnsafe } from '../../src/utils/fetch'

test('raiseIfUserProvidedUrlUnsafe', async () => {
    // Sync test cases with markettor/api/test/test_utils.py
    await raiseIfUserProvidedUrlUnsafe('https://google.com?q=20') // Safe
    await raiseIfUserProvidedUrlUnsafe('https://markettor.com') // Safe
    await raiseIfUserProvidedUrlUnsafe('https://markettor.com/foo/bar') // Safe, with path
    await raiseIfUserProvidedUrlUnsafe('https://markettor.com:443') // Safe, good port
    await raiseIfUserProvidedUrlUnsafe('https://1.1.1.1') // Safe, public IP
    await expect(raiseIfUserProvidedUrlUnsafe('')).rejects.toThrow(new FetchError('Invalid URL', 'markettor-host-guard'))
    await expect(raiseIfUserProvidedUrlUnsafe('@@@')).rejects.toThrow(
        new FetchError('Invalid URL', 'markettor-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('markettor.com')).rejects.toThrow(
        new FetchError('Invalid URL', 'markettor-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('ftp://markettor.com')).rejects.toThrow(
        new FetchError('Scheme must be either HTTP or HTTPS', 'markettor-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('http://localhost')).rejects.toThrow(
        new FetchError('Internal hostname', 'markettor-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('http://192.168.0.5')).rejects.toThrow(
        new FetchError('Internal hostname', 'markettor-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('http://0.0.0.0')).rejects.toThrow(
        new FetchError('Internal hostname', 'markettor-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('http://10.0.0.24')).rejects.toThrow(
        new FetchError('Internal hostname', 'markettor-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('http://172.20.0.21')).rejects.toThrow(
        new FetchError('Internal hostname', 'markettor-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('http://fgtggggzzggggfd.com')).rejects.toThrow(
        new FetchError('Invalid hostname', 'markettor-host-guard')
    )
})
