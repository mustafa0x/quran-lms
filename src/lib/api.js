function build_url(path, params = {}) {
    const url = new URL(path, window.location.origin)
    for (const [key, value] of Object.entries(params)) {
        if (value === undefined || value === null || value === '') continue
        url.searchParams.set(key, String(value))
    }
    return url.toString()
}

export async function api_get(path, params = {}) {
    const res = await fetch(build_url(path, params), {credentials: 'include'})
    if (!res.ok) return null
    return await res.json()
}

export async function api_request(method, path, data) {
    const res = await fetch(path, {
        method,
        headers: data ? {'Content-Type': 'application/json'} : {},
        body: data ? JSON.stringify(data) : undefined,
        credentials: 'include',
    })
    if (!res.ok) return false
    if (res.status === 204) return null
    return await res.json()
}
