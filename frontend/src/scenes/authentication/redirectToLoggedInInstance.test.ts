import { cleanedCookieSubdomain } from 'scenes/authentication/redirectToLoggedInInstance'

describe('redirectToLoggedInInstance', () => {
    test.each([
        ['handles null', null, null],
        ['handles the empty string', '', null],
        ['handles the sneaky string', '         ', null],
        ['handles not URLs', 'yo ho ho', null],
        ['handles EU', 'https://eu.markettor.com', 'eu'],
        ['handles app', 'https://app.markettor.com', null],
        ['handles US', 'https://us.markettor.com', 'us'],
        ['handles leading quotes', '"https://eu.markettor.com', 'eu'],
        ['handles trailing quotes', 'https://eu.markettor.com"', 'eu'],
        ['handles wrapping quotes', '"https://eu.markettor.com"', 'eu'],
        ['handles ports', 'https://us.markettor.com:8123', 'us'],
        ['handles longer urls', 'https://eu.markettor.com:1234?query=parameter#hashParam', 'eu'],
    ])('%s', (_name, cookie, expected) => {
        expect(cleanedCookieSubdomain(cookie)).toEqual(expected)
    })
})
