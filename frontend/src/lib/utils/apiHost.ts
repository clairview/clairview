export function apiHostOrigin(): string {
    const appOrigin = window.location.origin
    if (appOrigin === 'https://us.markettor.com') {
        return 'https://us.i.markettor.com'
    } else if (appOrigin === 'https://eu.markettor.com') {
        return 'https://eu.i.markettor.com'
    }
    return appOrigin
}

export function liveEventsHostOrigin(): string | null {
    const appOrigin = window.location.origin
    if (appOrigin === 'https://us.markettor.com') {
        return 'https://live.us.markettor.com'
    } else if (appOrigin === 'https://eu.markettor.com') {
        return 'https://live.eu.markettor.com'
    } else if (appOrigin === 'https://app.dev.markettor.dev') {
        return 'https://live.dev.markettor.dev'
    }
    return 'http://localhost:8666'
}
