<script>
import MoonIcon from '@lucide/svelte/icons/moon'
import SunIcon from '@lucide/svelte/icons/sun'

import {appstate} from '~/store.svelte.js'
import {Button} from '$ui/button/index.js'

const theme = $derived($appstate.theme)

function toggle_theme() {
    appstate.update(state => ({
        ...state,
        theme: state.theme === 'dark' ? 'light' : 'dark',
    }))
}
</script>

<Button
    variant="ghost"
    size="icon"
    onclick={toggle_theme}
    data-testid="button-theme-toggle"
    aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
>
    {#if theme === 'light'}
        <MoonIcon class="h-5 w-5" />
    {:else}
        <SunIcon class="h-5 w-5" />
    {/if}
</Button>
