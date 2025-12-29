import {debounce} from 'components'
import * as kv from 'idb-keyval'
import {writable} from 'svelte/store'

const default_state = {
    theme: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light',
    fun_day_target: 20,
}

export const appstate = writable(default_state)

export const session = writable({
    loaded: false,
})
;(async function init() {
    const appstate_idb = await kv.get('appstate')
    if (appstate_idb) appstate.set({...default_state, ...appstate_idb})

    session.update(v => ({...v, loaded: true}))

    appstate.subscribe(state => {
        document.documentElement.classList.toggle('dark', state.theme === 'dark')
    })

    appstate.subscribe(
        debounce(data => {
            kv.set('appstate', data)
        }, 200),
    )
})()
