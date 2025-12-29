<PageHeader title="Monthly Points" description="Track student points and achievements" />

<div class="space-y-6">
    <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
            <Button variant="ghost" size="icon" onclick={() => navigate_month(-1)} data-testid="button-prev-month-points">
                <ChevronLeftIcon class="h-4 w-4" />
            </Button>
            <h2 class="text-lg font-semibold">{month_label}</h2>
            <Button variant="ghost" size="icon" onclick={() => navigate_month(1)} data-testid="button-next-month-points">
                <ChevronRightIcon class="h-4 w-4" />
            </Button>
        </div>
    </div>

    <div class="grid gap-4 sm:grid-cols-4">
        <Card.Root>
            <Card.Content class="p-6">
                <p class="text-sm text-muted-foreground">Total Points Earned</p>
                <p class="text-3xl font-bold">{total_points}</p>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-6">
                <p class="text-sm text-muted-foreground">Average Points</p>
                <p class="text-3xl font-bold">{avg_points}</p>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-6">
                <p class="text-sm text-muted-foreground">Highest Score</p>
                <p class="text-3xl font-bold">{max_points}</p>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-6">
                <p class="text-sm text-muted-foreground">Fun Day Target</p>
                <p class="text-3xl font-bold">{fun_day_target}</p>
                <p class="text-xs text-muted-foreground">Avg {target_delta_label}</p>
            </Card.Content>
        </Card.Root>
    </div>

    {#if top_three.length > 0}
        <Card.Root>
            <Card.Header>
                <Card.Title class="flex items-center gap-2">
                    <TrophyIcon class="h-5 w-5 text-yellow-500" />
                    Top Performers
                </Card.Title>
            </Card.Header>
            <Card.Content>
                <div class="flex items-end justify-center gap-4 py-4">
                    {#if top_three[1]}
                        <div class="flex flex-col items-center">
                            <div class="flex h-12 w-12 items-center justify-center rounded-full bg-gray-200 text-lg font-bold text-gray-600 dark:bg-gray-700 dark:text-gray-300">
                                {top_three[1].student?.name?.charAt(0) ?? '?'}
                            </div>
                            <MedalIcon class="mt-2 h-6 w-6 text-gray-400" />
                            <p class="mt-1 text-sm font-medium">{top_three[1].student?.name ?? 'Unknown'}</p>
                            <p class="text-2xl font-bold">{top_three[1].totalPoints}</p>
                            <div class="mt-2 h-16 w-20 rounded-t-md bg-gray-200 dark:bg-gray-700"></div>
                        </div>
                    {/if}

                    {#if top_three[0]}
                        <div class="flex flex-col items-center">
                            <div class="flex h-14 w-14 items-center justify-center rounded-full bg-yellow-100 text-xl font-bold text-yellow-600 dark:bg-yellow-900/30">
                                {top_three[0].student?.name?.charAt(0) ?? '?'}
                            </div>
                            <TrophyIcon class="mt-2 h-7 w-7 text-yellow-500" />
                            <p class="mt-1 text-sm font-semibold">{top_three[0].student?.name ?? 'Unknown'}</p>
                            <p class="text-3xl font-bold">{top_three[0].totalPoints}</p>
                            <div class="mt-2 h-24 w-24 rounded-t-md bg-yellow-100 dark:bg-yellow-900/30"></div>
                        </div>
                    {/if}

                    {#if top_three[2]}
                        <div class="flex flex-col items-center">
                            <div class="flex h-11 w-11 items-center justify-center rounded-full bg-amber-100 text-lg font-bold text-amber-600 dark:bg-amber-900/30">
                                {top_three[2].student?.name?.charAt(0) ?? '?'}
                            </div>
                            <AwardIcon class="mt-2 h-5 w-5 text-amber-600" />
                            <p class="mt-1 text-sm font-medium">{top_three[2].student?.name ?? 'Unknown'}</p>
                            <p class="text-xl font-bold">{top_three[2].totalPoints}</p>
                            <div class="mt-2 h-12 w-16 rounded-t-md bg-amber-100 dark:bg-amber-900/30"></div>
                        </div>
                    {/if}
                </div>
            </Card.Content>
        </Card.Root>
    {/if}

    <Card.Root>
        <Card.Header>
            <Card.Title>Point Breakdown</Card.Title>
        </Card.Header>
        <Card.Content>
            {#if is_loading}
                <div class="space-y-3">
                    {#each Array.from({length: 5}) as _, index (index)}
                        <Skeleton class="h-12 w-full" />
                    {/each}
                </div>
            {:else}
                {#snippet cell(points, column)}
                    {#if column.key === 'rank'}
                        {@const rank = sorted_points.findIndex(item => item.id === points.id) + 1}
                        <span class="font-bold text-muted-foreground">
                            {#if rank === 1}
                                <TrophyIcon class="h-5 w-5 text-yellow-500" />
                            {:else if rank === 2}
                                <MedalIcon class="h-5 w-5 text-gray-400" />
                            {:else if rank === 3}
                                <AwardIcon class="h-5 w-5 text-amber-600" />
                            {:else}
                                {rank}
                            {/if}
                        </span>
                    {:else if column.key === 'student'}
                        <div class="flex items-center gap-3">
                            <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-sm font-medium text-primary">
                                {(points.student?.name ?? '?').charAt(0).toUpperCase()}
                            </div>
                            <span class="font-medium">{points.student?.name ?? 'Unknown'}</span>
                        </div>
                    {:else if column.key === 'new_work'}
                        <span class="font-medium">{points.newWorkPoints}</span>
                    {:else if column.key === 'front_work'}
                        <span class="font-medium">{points.frontWorkPoints}</span>
                    {:else if column.key === 'back_work'}
                        <span class="font-medium">{points.backWorkPoints}</span>
                    {:else if column.key === 'extra'}
                        <span class="font-medium">{points.extraWorkPoints}</span>
                    {:else if column.key === 'attendance'}
                        <span class="font-medium">{points.attendancePoints}</span>
                    {:else if column.key === 'behavior'}
                        <span class="font-medium">{points.behaviorPoints}</span>
                    {:else if column.key === 'total'}
                        <div class="flex items-center justify-end gap-2">
                            <StarIcon class="h-4 w-4 text-yellow-500" />
                            <span class="text-lg font-bold">{points.totalPoints}</span>
                        </div>
                    {/if}
                {/snippet}

                <DataTable
                    {columns}
                    data={sorted_points}
                    {cell}
                    get_row_key={row_key}
                    test_id_prefix="points"
                    is_loading={is_loading}
                    empty_message="No points recorded for this month"
                />
            {/if}
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Header class="pb-3">
            <Card.Title class="text-base">Point System</Card.Title>
        </Card.Header>
        <Card.Content>
            <div class="grid gap-2 text-sm sm:grid-cols-2 lg:grid-cols-3">
                {#each point_rules as item (item.label)}
                    <div class="flex items-center justify-between rounded-md bg-muted/50 p-2">
                        <span class="text-muted-foreground">{item.label}</span>
                        <span class="flex items-center gap-1 font-medium">
                            <StarIcon class="h-3 w-3 text-yellow-500" />
                            {item.points}
                        </span>
                    </div>
                {/each}
            </div>
        </Card.Content>
    </Card.Root>
</div>

<script>
import AwardIcon from '@lucide/svelte/icons/award'
import ChevronLeftIcon from '@lucide/svelte/icons/chevron-left'
import ChevronRightIcon from '@lucide/svelte/icons/chevron-right'
import MedalIcon from '@lucide/svelte/icons/medal'
import StarIcon from '@lucide/svelte/icons/star'
import TrophyIcon from '@lucide/svelte/icons/trophy'

import {api_get} from '$lib/api.js'
import {add_months, format_month_key, format_month_year} from '$lib/date.js'
import {appstate} from '~/store.svelte.js'
import {Button} from '$ui/button/index.js'
import * as Card from '$ui/card/index.js'
import {Skeleton} from '$ui/skeleton/index.js'
import DataTable from '$lib/components/data-table.svelte'
import PageHeader from '$lib/components/page-header.svelte'

let current_month = $state(new Date())
let points_data = $state([])
let is_loading = $state(true)

const fun_day_target = $derived($appstate.fun_day_target ?? 0)

const month_key = $derived(format_month_key(current_month))
const month_label = $derived(format_month_year(current_month))

const sorted_points = $derived([...points_data].sort((a, b) => b.totalPoints - a.totalPoints))
const top_three = $derived(sorted_points.slice(0, 3))

const total_points = $derived(points_data.reduce((sum, points) => sum + points.totalPoints, 0))
const avg_points = $derived(points_data.length > 0 ? Math.round(total_points / points_data.length) : 0)
const max_points = $derived(points_data.length > 0 ? Math.max(...points_data.map(points => points.totalPoints)) : 0)
const target_delta = $derived(avg_points - fun_day_target)
const target_delta_label = $derived(
    fun_day_target
        ? `${target_delta >= 0 ? '+' : ''}${target_delta} vs target`
        : 'Set a target in settings',
)

const columns = [
    {key: 'rank', header: '#'},
    {key: 'student', header: 'Student'},
    {key: 'new_work', header: 'New Work', class_name: 'text-center'},
    {key: 'front_work', header: 'Front Work', class_name: 'text-center'},
    {key: 'back_work', header: 'Back Work', class_name: 'text-center'},
    {key: 'extra', header: 'Extra', class_name: 'text-center'},
    {key: 'attendance', header: 'Attendance', class_name: 'text-center'},
    {key: 'behavior', header: 'Behavior', class_name: 'text-center'},
    {key: 'total', header: 'Total', class_name: 'text-right'},
]

const point_rules = [
    {label: 'New Work Pass', points: 1},
    {label: 'Front Work Pass', points: 1},
    {label: 'Back Work Pass', points: 1},
    {label: 'Extra Work Pass', points: 1},
    {label: 'Attendance', points: 1},
    {label: 'Behavior', points: 1},
]

function row_key(points) {
    return points.id
}

async function load_points() {
    is_loading = true
    points_data = (await api_get('/api/points', {month: month_key})) ?? []
    is_loading = false
}

function navigate_month(direction) {
    current_month = add_months(current_month, direction)
    load_points()
}

;(async () => {
    await load_points()
})()
</script>
