<script module>
import Attendance from '~/routes/Attendance.svelte'
import Dashboard from '~/routes/Dashboard.svelte'
import Homework from '~/routes/Homework.svelte'
import Lessons from '~/routes/Lessons.svelte'
import Muraja from '~/routes/Muraja.svelte'
import Points from '~/routes/Points.svelte'
import Reports from '~/routes/Reports.svelte'
import Settings from '~/routes/Settings.svelte'
import Students from '~/routes/Students.svelte'
import Teachers from '~/routes/Teachers.svelte'

export const routes = [
    ['/', Dashboard],
    ['/students', Students],
    ['/teachers', Teachers],
    ['/lessons', Lessons],
    ['/muraja', Muraja],
    ['/attendance', Attendance],
    ['/homework', Homework],
    ['/reports', Reports],
    ['/points', Points],
    ['/settings', Settings],
]
</script>

<Sidebar.Provider style="--sidebar-width: 16rem; --sidebar-width-icon: 3rem;">
    <div class="flex min-h-dvh w-full">
        <AppSidebar />
        <Sidebar.Inset class="flex flex-1 flex-col">
            <header class="sticky top-0 z-50 flex h-14 items-center justify-between gap-4 border-b bg-background px-4">
                <Sidebar.Trigger data-testid="button-sidebar-toggle" />
                <ThemeToggle />
            </header>
            <main class="flex-1 overflow-auto p-6">
                {#if ActiveComponent}
                    {#key $route.url.pathname}
                        <ActiveComponent data={route_data} />
                    {/key}
                {/if}
            </main>
        </Sidebar.Inset>
    </div>
</Sidebar.Provider>

<ModeWatcher />
<Toaster richColors position={toast_position} />
<Tooltip />

<div class={['request-indicator', $is_navigating && 'active']}></div>

{#if show_render_scan}
    <RenderScan hideIcon />
{/if}

<script>
import {Tooltip} from 'components'
import {ModeWatcher} from 'mode-watcher'
import {RenderScan} from 'svelte-render-scan'
import {Toaster} from 'svelte-sonner'

import NotFound from '~/routes/NotFound.svelte'
import AppSidebar from '$lib/components/app-sidebar.svelte'
import ThemeToggle from '$lib/components/theme-toggle.svelte'
import * as Sidebar from '$ui/sidebar/index.js'

const {Component, route_data, is_404} = $props()
const {route, is_navigating} = window.navgo

const ActiveComponent = $derived(is_404 ? NotFound : Component)
const toast_position = document.dir === 'rtl' ? 'top-left' : 'top-right'
const show_render_scan = window.__DEBUG__ && import.meta.env.VITE_RENDER_SCAN_ON
</script>
