<PageHeader title="Homework Tracking" description="Track daily homework completion status" />

<div class="space-y-6">
    <div class="flex items-center gap-2">
        <CalendarIcon class="h-5 w-5 text-muted-foreground" />
        <Input
            type="date"
            class="w-auto"
            bind:value={selected_date}
            onchange={handle_date_change}
            data-testid="input-homework-date"
        />
    </div>

    <div class="grid gap-4 sm:grid-cols-4">
        <Card.Root>
            <Card.Content class="p-4">
                <p class="text-sm text-muted-foreground">Total Students</p>
                <p class="text-2xl font-bold">{active_students.length}</p>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-4">
                <p class="text-sm text-muted-foreground">Passed</p>
                <p class="text-2xl font-bold text-green-600 dark:text-green-400">{passed_count}</p>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-4">
                <p class="text-sm text-muted-foreground">Not Passed</p>
                <p class="text-2xl font-bold text-red-600 dark:text-red-400">{failed_count}</p>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-4">
                <p class="text-sm text-muted-foreground">Pass Rate</p>
                <p class="text-2xl font-bold">{pass_rate}%</p>
            </Card.Content>
        </Card.Root>
    </div>

    <Card.Root>
        <Card.Header class="pb-3">
            <Card.Title class="flex items-center gap-2 text-lg font-semibold">
                <ClipboardIcon class="h-5 w-5" />
                Homework Status - {formatted_date}
            </Card.Title>
        </Card.Header>
        <Card.Content>
            {#if is_loading}
                <div class="space-y-3">
                    {#each Array.from({length: 5}) as _, index (index)}
                        <div class="flex items-center justify-between p-3">
                            <div class="flex items-center gap-3">
                                <Skeleton class="h-10 w-10 rounded-full" />
                                <Skeleton class="h-5 w-32" />
                            </div>
                            <Skeleton class="h-9 w-24" />
                        </div>
                    {/each}
                </div>
            {:else if active_students.length > 0}
                <div class="space-y-2">
                    {#each active_students as student (student.id)}
                        {@const homework = get_homework_for_student(student.id)}
                        {@const status = homework ? (homework.passed ? 'passed' : 'failed') : 'pending'}
                        <div class="flex items-center justify-between rounded-md border p-3" data-testid={`homework-row-${student.id}`}>
                            <div class="flex items-center gap-3">
                                <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-sm font-medium text-primary">
                                    {student.name.charAt(0).toUpperCase()}
                                </div>
                                <div>
                                    <p class="font-medium">{student.name}</p>
                                    <p class="text-xs text-muted-foreground">Juz {student.currentJuz}</p>
                                </div>
                            </div>

                            <div class="flex items-center gap-3">
                                {#if status !== 'pending'}
                                    <StatusBadge status={status === 'passed' ? 'success' : 'error'}>
                                        {status === 'passed' ? 'Passed' : 'Not Passed'}
                                    </StatusBadge>
                                {/if}
                                <div class="flex gap-1">
                                    <Button
                                        variant={status === 'passed' ? 'default' : 'outline'}
                                        size="icon"
                                        onclick={() => status !== 'passed' && toggle_homework(student.id, true)}
                                        disabled={is_toggling}
                                        data-testid={`button-homework-pass-${student.id}`}
                                    >
                                        <CheckIcon class="h-4 w-4" />
                                    </Button>
                                    <Button
                                        variant={status === 'failed' ? 'destructive' : 'outline'}
                                        size="icon"
                                        onclick={() => status !== 'failed' && toggle_homework(student.id, false)}
                                        disabled={is_toggling}
                                        data-testid={`button-homework-fail-${student.id}`}
                                    >
                                        <XIcon class="h-4 w-4" />
                                    </Button>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            {:else}
                <div class="flex h-32 items-center justify-center">
                    <p class="text-sm text-muted-foreground">No active students found</p>
                </div>
            {/if}
        </Card.Content>
    </Card.Root>
</div>

<script>
import CalendarIcon from '@lucide/svelte/icons/calendar'
import CheckIcon from '@lucide/svelte/icons/check'
import ClipboardIcon from '@lucide/svelte/icons/clipboard-check'
import XIcon from '@lucide/svelte/icons/x'
import {toast} from 'svelte-sonner'

import {api_get, api_request} from '$lib/api.js'
import PageHeader from '$lib/components/page-header.svelte'
import StatusBadge from '$lib/components/status-badge.svelte'
import {format_date_input, format_readable_date} from '$lib/date.js'
import {Button} from '$ui/button/index.js'
import * as Card from '$ui/card/index.js'
import {Input} from '$ui/input/index.js'
import {Skeleton} from '$ui/skeleton/index.js'

let students = $state([])
let homework_records = $state([])
let is_loading = $state(true)
let is_toggling = $state(false)
let selected_date = $state(format_date_input(new Date()))

const active_students = $derived(students.filter(student => student.status === 'active'))

const passed_count = $derived(homework_records.filter(record => record.passed).length)
const failed_count = $derived(homework_records.filter(record => !record.passed).length)
const pass_rate = $derived(
    homework_records.length > 0 ? Math.round((passed_count / homework_records.length) * 100) : 0,
)

const formatted_date = $derived(format_readable_date(new Date(selected_date)))

function get_homework_for_student(student_id) {
    return homework_records.find(record => record.studentId === student_id)
}

async function load_students() {
    students = (await api_get('/api/students')) ?? []
}

async function load_homework() {
    is_loading = true
    homework_records = (await api_get('/api/homework', {date: selected_date})) ?? []
    is_loading = false
}

async function toggle_homework(student_id, passed) {
    is_toggling = true
    const response = await api_request('POST', '/api/homework', {
        studentId: student_id,
        date: selected_date,
        passed,
    })

    if (response === false) {
        toast.error('Failed to update homework status')
        is_toggling = false
        return
    }

    await load_homework()
    is_toggling = false
}

function handle_date_change() {
    load_homework()
}

;(async () => {
    await load_students()
    await load_homework()
})()
</script>
