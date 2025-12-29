{#snippet actions()}
    <Button
        variant="outline"
        onclick={recalculate}
        disabled={is_recalculating}
        data-testid="button-recalculate-muraja"
    >
        <RefreshIcon class="mr-2 h-4 w-4 {is_recalculating ? 'animate-spin' : ''}" />
        Recalculate All
    </Button>
{/snippet}

<PageHeader
    title="Muraja'ah Management"
    description="Track and manage student revision schedules"
    {actions}
/>

<div class="space-y-6">
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card.Root>
            <Card.Content class="p-6">
                <div class="flex items-center gap-4">
                    <div class="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                        <RefreshIcon class="h-6 w-6 text-primary" />
                    </div>
                    <div>
                        <p class="text-sm text-muted-foreground">Active Schedules</p>
                        <p class="text-2xl font-bold">{active_count}</p>
                    </div>
                </div>
            </Card.Content>
        </Card.Root>

        <Card.Root>
            <Card.Content class="p-6">
                <div class="flex items-center gap-4">
                    <div class="flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
                        <CheckCircleIcon class="h-6 w-6 text-green-600 dark:text-green-400" />
                    </div>
                    <div>
                        <p class="text-sm text-muted-foreground">On Track</p>
                        <p class="text-2xl font-bold text-green-600 dark:text-green-400">{on_track_count}</p>
                    </div>
                </div>
            </Card.Content>
        </Card.Root>

        <Card.Root>
            <Card.Content class="p-6">
                <div class="flex items-center gap-4">
                    <div class="flex h-12 w-12 items-center justify-center rounded-full bg-amber-100 dark:bg-amber-900/30">
                        <AlertTriangleIcon class="h-6 w-6 text-amber-600 dark:text-amber-400" />
                    </div>
                    <div>
                        <p class="text-sm text-muted-foreground">Overdue</p>
                        <p class="text-2xl font-bold text-amber-600 dark:text-amber-400">{overdue_count}</p>
                    </div>
                </div>
            </Card.Content>
        </Card.Root>

        <Card.Root>
            <Card.Content class="p-6">
                <div class="flex items-center justify-center">
                    <ProgressRing
                        value={on_track_count}
                        max={active_count || 1}
                        size={80}
                        stroke_width={8}
                        label="Compliance"
                    />
                </div>
            </Card.Content>
        </Card.Root>
    </div>

    <Card.Root>
        <Card.Header class="pb-3">
            <Card.Title class="text-base">Daily Load Rules</Card.Title>
        </Card.Header>
        <Card.Content>
            <div class="grid gap-2 text-sm sm:grid-cols-2 lg:grid-cols-4">
                <div class="flex justify-between rounded-md bg-muted/50 p-2">
                    <span class="text-muted-foreground">1-2 Juz</span>
                    <span class="font-medium">0.25 Juz/day</span>
                </div>
                <div class="flex justify-between rounded-md bg-muted/50 p-2">
                    <span class="text-muted-foreground">3-6 Juz</span>
                    <span class="font-medium">0.5 Juz/day</span>
                </div>
                <div class="flex justify-between rounded-md bg-muted/50 p-2">
                    <span class="text-muted-foreground">6-10 Juz</span>
                    <span class="font-medium">1 Juz/day</span>
                </div>
                <div class="flex justify-between rounded-md bg-muted/50 p-2">
                    <span class="text-muted-foreground">11-15 Juz</span>
                    <span class="font-medium">1.5 Juz/day</span>
                </div>
                <div class="flex justify-between rounded-md bg-muted/50 p-2">
                    <span class="text-muted-foreground">16-20 Juz</span>
                    <span class="font-medium">2 Juz/day</span>
                </div>
                <div class="flex justify-between rounded-md bg-muted/50 p-2">
                    <span class="text-muted-foreground">21-25 Juz</span>
                    <span class="font-medium">2.5 Juz/day</span>
                </div>
                <div class="flex justify-between rounded-md bg-muted/50 p-2">
                    <span class="text-muted-foreground">26-30 Juz</span>
                    <span class="font-medium">3 Juz/day</span>
                </div>
            </div>
        </Card.Content>
    </Card.Root>

    {#snippet cell(schedule, column)}
        {#if column.key === 'student'}
            <div class="flex items-center gap-3">
                <div class="flex h-9 w-9 items-center justify-center rounded-full bg-primary/10 text-sm font-medium text-primary">
                    {(schedule.student?.name ?? '?').charAt(0).toUpperCase()}
                </div>
                <div>
                    <p class="font-medium">{schedule.student?.name ?? 'Unknown'}</p>
                    <p class="text-xs text-muted-foreground">{schedule.student?.totalJuzMemorized ?? 0} Juz memorized</p>
                </div>
            </div>
        {:else if column.key === 'daily_load'}
            <span class="font-medium">{get_muraja_daily_load(schedule.student?.totalJuzMemorized ?? 0)} Juz/day</span>
        {:else if column.key === 'cycle'}
            <span class="text-muted-foreground">{schedule.cycleLengthDays} days</span>
        {:else if column.key === 'next_due'}
            <div class="flex items-center gap-2">
                <ClockIcon class="h-4 w-4 text-muted-foreground" />
                <span>{schedule.nextRevisionDueDate ?? 'Not scheduled'}</span>
            </div>
        {:else if column.key === 'status'}
            <StatusBadge status={get_muraja_status_type(schedule.overdue)}>
                {schedule.overdue ? 'Overdue' : 'On Track'}
            </StatusBadge>
        {:else if column.key === 'actions'}
            <Button
                variant="outline"
                size="sm"
                onclick={() => mark_complete(schedule.id)}
                disabled={marking_id === schedule.id}
                data-testid={`button-complete-muraja-${schedule.id}`}
            >
                <CheckCircleIcon class="mr-1 h-4 w-4" />
                Mark Complete
            </Button>
        {/if}
    {/snippet}

    <DataTable
        {columns}
        data={muraja_schedules}
        {cell}
        get_row_key={row_key}
        test_id_prefix="muraja"
        is_loading={is_loading}
        empty_message="No muraja schedules found"
    />
</div>

<script>
import AlertTriangleIcon from '@lucide/svelte/icons/alert-triangle'
import CheckCircleIcon from '@lucide/svelte/icons/check-circle'
import ClockIcon from '@lucide/svelte/icons/clock'
import RefreshIcon from '@lucide/svelte/icons/refresh-cw'

import {toast} from 'svelte-sonner'

import {api_get, api_request} from '$lib/api.js'
import {get_muraja_daily_load} from '$lib/quran.js'
import {Button} from '$ui/button/index.js'
import * as Card from '$ui/card/index.js'
import DataTable from '$lib/components/data-table.svelte'
import PageHeader from '$lib/components/page-header.svelte'
import ProgressRing from '$lib/components/progress-ring.svelte'
import StatusBadge, {get_muraja_status_type} from '$lib/components/status-badge.svelte'

let muraja_schedules = $state([])
let is_loading = $state(true)
let is_recalculating = $state(false)
let marking_id = $state('')

const active_count = $derived(muraja_schedules.length)
const overdue_count = $derived(muraja_schedules.filter(schedule => schedule.overdue).length)
const on_track_count = $derived(muraja_schedules.filter(schedule => !schedule.overdue).length)

const columns = [
    {key: 'student', header: 'Student'},
    {key: 'daily_load', header: 'Daily Load'},
    {key: 'cycle', header: 'Cycle'},
    {key: 'next_due', header: 'Next Due'},
    {key: 'status', header: 'Status'},
    {key: 'actions', header: '', class_name: 'text-right'},
]

function row_key(schedule) {
    return schedule.id
}

async function load_muraja() {
    is_loading = true
    muraja_schedules = (await api_get('/api/muraja')) ?? []
    is_loading = false
}

async function recalculate() {
    is_recalculating = true
    const response = await api_request('POST', '/api/muraja/recalculate')
    if (response === false) {
        toast.error('Failed to recalculate schedules')
        is_recalculating = false
        return
    }
    toast.success("Muraja'ah schedules recalculated")
    is_recalculating = false
    await load_muraja()
}

async function mark_complete(schedule_id) {
    marking_id = schedule_id
    const response = await api_request('POST', `/api/muraja/${schedule_id}/complete`)
    if (response === false) {
        toast.error('Failed to mark as complete')
        marking_id = ''
        return
    }
    toast.success('Revision marked as complete')
    marking_id = ''
    await load_muraja()
}

;(async () => {
    await load_muraja()
})()
</script>
