import './css/tailwind.css'
import './css/base.css'
import './lib/preinit.js'

import Navgo from 'navgo'
import {hydrate} from 'svelte'

import {session} from '~/store.svelte.js'

import App, {routes} from './App.svelte'

const props = $state({Component: null, route_data: null, is_404: false})

function after_navigate(nav) {
    props.is_404 = nav.to.data?.__error?.status === 404
    props.route_data = nav.to.data
    props.Component = nav.to.route?.[1]
}

export const router = new Navgo(routes, {after_navigate})

const unsubscribe = session.subscribe(async s => {
    if (s.loaded) {
        await router.init()
        hydrate(App, {target: document.body, props})
        unsubscribe()
    }
})
