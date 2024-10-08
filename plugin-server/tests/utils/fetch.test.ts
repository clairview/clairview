import { FetchError } from 'node-fetch'

import { raiseIfUserProvidedUrlUnsafe } from '../../src/utils/fetch'

test('raiseIfUserProvidedUrlUnsafe', async () => {
    // Sync test cases with clairview/api/test/test_utils.py
    await raiseIfUserProvidedUrlUnsafe('https://google.com?q=20') // Safe
    await raiseIfUserProvidedUrlUnsafe('https://clairview.com') // Safe
    await raiseIfUserProvidedUrlUnsafe('https://clairview.com/foo/bar') // Safe, with path
    await raiseIfUserProvidedUrlUnsafe('https://clairview.com:443') // Safe, good port
    await raiseIfUserProvidedUrlUnsafe('https://1.1.1.1') // Safe, public IP
    await expect(raiseIfUserProvidedUrlUnsafe('')).rejects.toThrow(new FetchError('Invalid URL', 'clairview-host-guard'))
    await expect(raiseIfUserProvidedUrlUnsafe('@@@')).rejects.toThrow(
        new FetchError('Invalid URL', 'clairview-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('clairview.com')).rejects.toThrow(
        new FetchError('Invalid URL', 'clairview-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('ftp://clairview.com')).rejects.toThrow(
        new FetchError('Scheme must be either HTTP or HTTPS', 'clairview-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('http://localhost')).rejects.toThrow(
        new FetchError('Internal hostname', 'clairview-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('http://192.168.0.5')).rejects.toThrow(
        new FetchError('Internal hostname', 'clairview-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('http://0.0.0.0')).rejects.toThrow(
        new FetchError('Internal hostname', 'clairview-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('http://10.0.0.24')).rejects.toThrow(
        new FetchError('Internal hostname', 'clairview-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('http://172.20.0.21')).rejects.toThrow(
        new FetchError('Internal hostname', 'clairview-host-guard')
    )
    await expect(raiseIfUserProvidedUrlUnsafe('http://fgtggggzzggggfd.com')).rejects.toThrow(
        new FetchError('Invalid hostname', 'clairview-host-guard')
    )
})
