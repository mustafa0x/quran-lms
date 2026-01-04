<PageHeader title="Attendance" description="Track daily student attendance" />

<div class="space-y-6">
    <div class="max-w-sm">
        <Select.Root bind:value={selected_student} onValueChange={handle_student_change}>
            <Select.Trigger data-testid="select-attendance-student">
                <span data-slot="select-value">{student_label}</span>
            </Select.Trigger>
            <Select.Content>
                {#each active_students as student (student.id)}
                    <Select.Item value={student.id}>{student.name}</Select.Item>
                {/each}
            </Select.Content>
        </Select.Root>
    </div>

    {#if selected_student}
        <div class="grid gap-4 sm:grid-cols-3">
            <Card.Root>
                <Card.Content class="p-4">
                    <p class="text-sm text-muted-foreground">Present</p>
                    <p class="text-2xl font-bold text-green-600 dark:text-green-400">{present_days} days</p>
                </Card.Content>
            </Card.Root>
            <Card.Root>
                <Card.Content class="p-4">
                    <p class="text-sm text-muted-foreground">Absent</p>
                    <p class="text-2xl font-bold text-red-600 dark:text-red-400">{absent_days} days</p>
                </Card.Content>
            </Card.Root>
            <Card.Root>
                <Card.Content class="p-4">
                    <p class="text-sm text-muted-foreground">Attendance Rate</p>
                    <p class="text-2xl font-bold">{attendance_rate}%</p>
                </Card.Content>
            </Card.Root>
        </div>

        <Card.Root>
            <Card.Header class="flex flex-row items-center justify-between gap-4 space-y-0 pb-4">
                <Card.Title class="text-lg font-semibold">{month_label}</Card.Title>
                <div class="flex items-center gap-1">
                    <Button variant="ghost" size="icon" onclick={() => navigate_month(-1)} data-testid="button-prev-month">
                        <ChevronLeftIcon class="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="icon" onclick={() => navigate_month(1)} data-testid="button-next-month">
                        <ChevronRightIcon class="h-4 w-4" />
                    </Button>
                </div>
            </Card.Header>
            <Card.Content>
                {#if attendance_loading}
                    <div class="grid grid-cols-7 gap-2">
                        {#each week_days as day (day)}
                            <div class="p-2 text-center text-sm font-medium text-muted-foreground">{day}</div>
                        {/each}
                        {#each Array.from({length: 35}) as _, index (index)}
                            <Skeleton class="aspect-square rounded-md" />
                        {/each}
                    </div>
                {:else}
                    <div class="grid grid-cols-7 gap-2">
                        {#each week_days as day (day)}
                            <div class="p-2 text-center text-sm font-medium text-muted-foreground">{day}</div>
                        {/each}

                        {#each Array.from({length: month_offset}) as _, index (index)}
                            <div></div>
                        {/each}

                        {#each days_in_month as day (day.toISOString())}
                            {@const attendance = get_attendance_for_day(day)}
                            {@const is_today = is_same_day(day, today)}
                            {@const is_future = day > today}
                            <button
                                onclick={() => !is_future && toggle_attendance(day)}
                                disabled={is_future || is_toggling}
                                class="aspect-square flex flex-col items-center justify-center rounded-md border text-sm transition-colors
                                    {is_today ? 'border-primary' : 'border-transparent'}
                                    {is_future ? 'cursor-not-allowed opacity-50' : 'cursor-pointer hover-elevate'}
                                    {attendance?.present
                                        ? 'bg-green-100 dark:bg-green-900/30'
                                        : attendance && !attendance.present
                                        ? 'bg-red-100 dark:bg-red-900/30'
                                        : 'bg-muted/30'}"
                                data-testid={`attendance-day-${format_date_input(day)}`}
                            >
                                <span class="font-medium">{day.getDate()}</span>
                                {#if attendance}
                                    <span class="mt-0.5">
                                        {#if attendance.present}
                                            <CheckIcon class="h-3 w-3 text-green-600 dark:text-green-400" />
                                        {:else}
                                            <XIcon class="h-3 w-3 text-red-600 dark:text-red-400" />
                                        {/if}
                                    </span>
                                {/if}
                            </button>
                        {/each}
                    </div>
                {/if}
            </Card.Content>
        </Card.Root>

        <div class="flex items-center gap-6 text-sm">
            <div class="flex items-center gap-2">
                <div class="h-4 w-4 rounded bg-green-100 dark:bg-green-900/30"></div>
                <span class="text-muted-foreground">Present</span>
            </div>
            <div class="flex items-center gap-2">
                <div class="h-4 w-4 rounded bg-red-100 dark:bg-red-900/30"></div>
                <span class="text-muted-foreground">Absent</span>
            </div>
            <div class="flex items-center gap-2">
                <div class="h-4 w-4 rounded bg-muted/30"></div>
                <span class="text-muted-foreground">No record</span>
            </div>
        </div>
    {:else}
        <Card.Root>
            <Card.Content class="flex h-64 items-center justify-center">
                <p class="text-muted-foreground">Select a student to view attendance</p>
            </Card.Content>
        </Card.Root>
    {/if}
</div>

<script>
import CheckIcon from '@lucide/svelte/icons/check'
import ChevronLeftIcon from '@lucide/svelte/icons/chevron-left'
import ChevronRightIcon from '@lucide/svelte/icons/chevron-right'
import XIcon from '@lucide/svelte/icons/x'
import {toast} from 'svelte-sonner'

import {api_get, api_request} from '$lib/api.js'
import PageHeader from '$lib/components/page-header.svelte'
import {
    add_months,
    each_day_of_interval,
    end_of_month,
    format_date_input,
    format_month_year,
    is_same_day,
    start_of_month,
} from '$lib/date.js'
import {Button} from '$ui/button/index.js'
import * as Card from '$ui/card/index.js'
import * as Select from '$ui/select/index.js'
import {Skeleton} from '$ui/skeleton/index.js'

let students = $state([])
let attendance_records = $state([])
let students_loading = $state(true)
let attendance_loading = $state(false)
let is_toggling = $state(false)

let current_month = $state(new Date())
let selected_student = $state('')

const today = new Date()
const week_days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const month_start = $derived(start_of_month(current_month))
const month_end = $derived(end_of_month(current_month))
const days_in_month = $derived(each_day_of_interval(month_start, month_end))
const month_offset = $derived(month_start.getDay())
const month_label = $derived(format_month_year(current_month))

const active_students = $derived(students.filter(student => student.status === 'active'))
const student_label = $derived(
    selected_student
        ? active_students.find(student => student.id === selected_student)?.name ?? 'Select student'
        : 'Select a student',
)

const present_days = $derived(attendance_records.filter(record => record.present).length)
const absent_days = $derived(attendance_records.filter(record => !record.present).length)
const attendance_rate = $derived(
    attendance_records.length > 0
        ? Math.round((present_days / attendance_records.length) * 100)
        : 0,
)

function get_attendance_for_day(day) {
    return attendance_records.find(record => record.date === format_date_input(day))
}

async function load_students() {
    students_loading = true
    students = (await api_get('/api/students')) ?? []
    students_loading = false
}

async function load_attendance() {
    if (!selected_student) return
    attendance_loading = true
    attendance_records = (await api_get('/api/attendance', {
        studentId: selected_student,
        startDate: format_date_input(month_start),
        endDate: format_date_input(month_end),
    })) ?? []
    attendance_loading = false
}

async function toggle_attendance(day) {
    if (!selected_student) return
    is_toggling = true
    const existing = get_attendance_for_day(day)
    const response = await api_request('POST', '/api/attendance', {
        studentId: selected_student,
        date: format_date_input(day),
        present: existing ? !existing.present : true,
    })

    if (response === false) {
        toast.error('Failed to update attendance')
        is_toggling = false
        return
    }

    await load_attendance()
    is_toggling = false
}

function navigate_month(direction) {
    current_month = add_months(current_month, direction)
    load_attendance()
}

function handle_student_change() {
    load_attendance()
}

;(async () => {
    await load_students()
})()
</script>
