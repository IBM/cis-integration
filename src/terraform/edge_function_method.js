addEventListener('fetch', (event) => {
    const mutable_request = new Request(event.request);
    event.respondWith(redirectAndLog(mutable_request));
});

async function redirectAndLog(request) {
    const response = await redirectOrPass(request);
    return response;
}

async function getSite(request, site) {
    const url = new URL(request.url);
    // let our servers know what origin the request came from
    // https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-Host
    request.headers.set('X-Forwarded-Host', url.hostname);
    request.headers.set('host', site);
    url.hostname = site;
    url.protocol = "https:";
    response = fetch(url.toString(), request);
    console.log('Got getSite Request to ' + site, response);
    return response;
}

async function redirectOrPass(request) {
    const urlObject = new URL(request.url);

    let response = null;

    try {
        console.log('Got MAIN request', request);

        response = await getSite(request, 'demo-app.9y43h3pccht.us-south.codeengine.appdomain.cloud');
        console.log('Got MAIN response', response.status);
        return response;

    } catch (error) {
        // if no action found, play the regular request
        console.log('Got Error', error);
        return await fetch(request);

    }

}
