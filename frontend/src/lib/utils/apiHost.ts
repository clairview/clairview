export function apiHostOrigin(): string {
    const appOrigin = window.location.origin
    if (appOrigin === 'https://us.clairview.com') {
        return 'https://us.i.clairview.com'
    } else if (appOrigin === 'https://eu.clairview.com') {
        return 'https://eu.i.clairview.com'
    }
    return appOrigin
}

export function liveEventsHostOrigin(): string | null {
    const appOrigin = window.location.origin
    if (appOrigin === 'https://us.clairview.com') {
        return 'https://live.us.clairview.com'
    } else if (appOrigin === 'https://eu.clairview.com') {
        return 'https://live.eu.clairview.com'
    } else if (appOrigin === 'https://app.dev.clairview.dev') {
        return 'https://live.dev.clairview.dev'
    }
    return 'http://localhost:8666'
}
