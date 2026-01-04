<PageHeader title="Settings" description="Configure your application preferences" />

<div class="space-y-6">
    <Card.Root>
        <Card.Header>
            <Card.Title class="flex items-center gap-2">
                <SettingsIcon class="h-5 w-5" />
                Appearance
            </Card.Title>
            <Card.Description>Customize how the application looks</Card.Description>
        </Card.Header>
        <Card.Content class="space-y-6">
            <div class="space-y-3">
                <Label>Theme</Label>
                <div class="flex flex-wrap gap-3">
                    <Button
                        variant={theme === 'light' ? 'default' : 'outline'}
                        onclick={() => set_theme('light')}
                        class="flex-1 min-w-[120px]"
                        data-testid="button-theme-light"
                    >
                        <SunIcon class="mr-2 h-4 w-4" />
                        Light
                    </Button>
                    <Button
                        variant={theme === 'dark' ? 'default' : 'outline'}
                        onclick={() => set_theme('dark')}
                        class="flex-1 min-w-[120px]"
                        data-testid="button-theme-dark"
                    >
                        <MoonIcon class="mr-2 h-4 w-4" />
                        Dark
                    </Button>
                </div>
            </div>
            <div class="space-y-2">
                <Label>Fun Day Point Target</Label>
                <Input
                    type="number"
                    min="0"
                    class="max-w-xs"
                    value={fun_day_target}
                    oninput={update_fun_day_target}
                    data-testid="input-fun-day-target"
                />
                <p class="text-xs text-muted-foreground">Used to compare monthly point averages.</p>
            </div>
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Header>
            <Card.Title>About</Card.Title>
            <Card.Description>Application information</Card.Description>
        </Card.Header>
        <Card.Content class="space-y-4">
            <div class="flex justify-between">
                <span class="text-muted-foreground">Application</span>
                <span class="font-medium">Quran Memorization Tracker</span>
            </div>
            <div class="flex justify-between">
                <span class="text-muted-foreground">Version</span>
                <span class="font-medium">1.0.0</span>
            </div>
            <div class="flex justify-between">
                <span class="text-muted-foreground">Purpose</span>
                <span class="font-medium">Track Quran memorization progress</span>
            </div>
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Header>
            <Card.Title>Point System Rules</Card.Title>
            <Card.Description>How points are calculated</Card.Description>
        </Card.Header>
        <Card.Content>
            <div class="space-y-3 text-sm">
                {#each point_rules as rule (rule.label)}
                    <div class="flex justify-between rounded-md bg-muted/50 p-3">
                        <span>{rule.label}</span>
                        <span class="font-medium">{rule.points} point</span>
                    </div>
                {/each}
            </div>
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Header>
            <Card.Title>Muraja'ah Load Rules</Card.Title>
            <Card.Description>Daily revision based on memorization level</Card.Description>
        </Card.Header>
        <Card.Content>
            <div class="space-y-3 text-sm">
                {#each muraja_rules as rule (rule.label)}
                    <div class="flex justify-between rounded-md bg-muted/50 p-3">
                        <span>{rule.label}</span>
                        <span class="font-medium">{rule.value}</span>
                    </div>
                {/each}
            </div>
        </Card.Content>
    </Card.Root>
</div>

<script>
import MoonIcon from '@lucide/svelte/icons/moon'
import SettingsIcon from '@lucide/svelte/icons/settings'
import SunIcon from '@lucide/svelte/icons/sun'

import {appstate} from '~/store.svelte.js'
import PageHeader from '$lib/components/page-header.svelte'
import {Button} from '$ui/button/index.js'
import * as Card from '$ui/card/index.js'
import {Input} from '$ui/input/index.js'
import {Label} from '$ui/label/index.js'

const theme = $derived($appstate.theme)
const fun_day_target = $derived($appstate.fun_day_target)

const point_rules = [
    {label: 'New Work Pass', points: 1},
    {label: 'Front Work Pass', points: 1},
    {label: 'Back Work Pass', points: 1},
    {label: 'Extra Work Pass', points: 1},
    {label: 'Attendance', points: 1},
    {label: 'Behavior', points: 1},
]

const muraja_rules = [
    {label: '1-2 Juz memorized', value: '0.25 Juz/day'},
    {label: '3-6 Juz memorized', value: '0.5 Juz/day'},
    {label: '6-10 Juz memorized', value: '1 Juz/day'},
    {label: '11-15 Juz memorized', value: '1.5 Juz/day'},
    {label: '16-20 Juz memorized', value: '2 Juz/day'},
    {label: '21-25 Juz memorized', value: '2.5 Juz/day'},
    {label: '26-30 Juz memorized', value: '3 Juz/day'},
]

function set_theme(next_theme) {
    appstate.update(state => ({
        ...state,
        theme: next_theme,
    }))
}

function update_fun_day_target(event) {
    const value = Number(event.currentTarget.value || 0)
    appstate.update(state => ({
        ...state,
        fun_day_target: Number.isNaN(value) ? 0 : value,
    }))
}
</script>
