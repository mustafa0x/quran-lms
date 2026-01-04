{#snippet actions()}
    <Button onclick={open_form} data-testid="button-add-lesson">
        <PlusIcon class="mr-2 h-4 w-4" />
        Log Lesson
    </Button>
{/snippet}

<PageHeader
    title="Daily Lessons"
    description="Log and track daily memorization lessons"
    {actions}
/>

<div class="space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div class="flex items-center gap-2">
            <CalendarIcon class="h-5 w-5 text-muted-foreground" />
            <Input
                type="date"
                class="w-auto"
                bind:value={selected_date}
                data-testid="input-lesson-date-filter"
                onchange={handle_date_change}
            />
        </div>
    </div>

    <div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <Card.Root>
            <Card.Content class="p-4">
                <p class="text-sm text-muted-foreground">Total Lessons</p>
                <p class="text-2xl font-bold">{lesson_counts.all}</p>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-4">
                <p class="text-sm text-muted-foreground">New Lessons</p>
                <p class="text-2xl font-bold text-blue-600 dark:text-blue-400">{lesson_counts.new}</p>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-4">
                <p class="text-sm text-muted-foreground">Front Revisions</p>
                <p class="text-2xl font-bold text-amber-600 dark:text-amber-400">{lesson_counts.front}</p>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-4">
                <p class="text-sm text-muted-foreground">Muraja'ah</p>
                <p class="text-2xl font-bold text-green-600 dark:text-green-400">{lesson_counts.muraja}</p>
            </Card.Content>
        </Card.Root>
    </div>

    <Tabs.Root bind:value={filter_type}>
        <Tabs.List>
            <Tabs.Trigger value="ALL" data-testid="tab-filter-all">All ({lesson_counts.all})</Tabs.Trigger>
            <Tabs.Trigger value="NEW" data-testid="tab-filter-new">New</Tabs.Trigger>
            <Tabs.Trigger value="FRONT_REVISION" data-testid="tab-filter-front">Front</Tabs.Trigger>
            <Tabs.Trigger value="MURAJAH" data-testid="tab-filter-muraja">Muraja'ah</Tabs.Trigger>
        </Tabs.List>
    </Tabs.Root>

    {#snippet cell(lesson, column)}
        {#if column.key === 'student'}
            <div class="flex items-center gap-2">
                <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-sm font-medium text-primary">
                    {(lesson.student?.name ?? '?').charAt(0).toUpperCase()}
                </div>
                <span class="font-medium">{lesson.student?.name ?? 'Unknown'}</span>
            </div>
        {:else if column.key === 'lesson_type'}
            <StatusBadge status={lesson.lessonType === 'NEW' ? 'info' : lesson.lessonType === 'FRONT_REVISION' ? 'warning' : 'success'}>
                {lesson_type_labels[lesson.lessonType]}
            </StatusBadge>
        {:else if column.key === 'content'}
            <span class="text-sm">{lesson.surah} ({lesson.ayahStart}-{lesson.ayahEnd})</span>
        {:else if column.key === 'juz'}
            Juz {lesson.juz}
        {:else if column.key === 'rating'}
            <StatusBadge status={get_rating_status_type(lesson.rating)}>{lesson.rating}</StatusBadge>
        {:else if column.key === 'extra'}
            {#if lesson.extraWork}
                <StatusBadge status="success">Yes</StatusBadge>
            {:else}
                <span class="text-muted-foreground">-</span>
            {/if}
        {/if}
    {/snippet}

    <DataTable
        {columns}
        data={filtered_lessons}
        {cell}
        get_row_key={row_key}
        test_id_prefix="lessons"
        is_loading={is_loading}
        empty_message="No lessons logged for this date. Start by logging a lesson."
    />
</div>

<Dialog.Root bind:open={is_form_open}>
    <Dialog.Content class="max-w-lg">
        <Dialog.Header>
            <Dialog.Title>Log New Lesson</Dialog.Title>
        </Dialog.Header>
        <form class="space-y-4" onsubmit={submit_form}>
            <div class="space-y-2">
                <Label>Student</Label>
                <Select.Root bind:value={form_state.student_id}>
                    <Select.Trigger data-testid="select-lesson-student">
                        <span data-slot="select-value">{student_label}</span>
                    </Select.Trigger>
                    <Select.Content>
                        {#each active_students as student (student.id)}
                            <Select.Item value={student.id}>{student.name}</Select.Item>
                        {/each}
                    </Select.Content>
                </Select.Root>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                    <Label>Date</Label>
                    <Input type="date" bind:value={form_state.date} data-testid="input-lesson-date" />
                </div>
                <div class="space-y-2">
                    <Label>Lesson Type</Label>
                    <Select.Root bind:value={form_state.lesson_type}>
                        <Select.Trigger data-testid="select-lesson-type">
                            <span data-slot="select-value">{lesson_type_label}</span>
                        </Select.Trigger>
                        <Select.Content>
                            {#each lesson_type_options as option (option.value)}
                                <Select.Item value={option.value}>{option.label}</Select.Item>
                            {/each}
                        </Select.Content>
                    </Select.Root>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                    <Label>Juz</Label>
                    <Input type="number" min="1" max="30" bind:value={form_state.juz} data-testid="input-lesson-juz" />
                </div>
                <div class="space-y-2">
                    <Label>Surah</Label>
                    <Select.Root bind:value={form_state.surah}>
                        <Select.Trigger data-testid="select-lesson-surah">
                            <span data-slot="select-value">{surah_label}</span>
                        </Select.Trigger>
                        <Select.Content class="max-h-60">
                            {#each surah_options as surah (surah.value)}
                                <Select.Item value={surah.value}>{surah.label}</Select.Item>
                            {/each}
                        </Select.Content>
                    </Select.Root>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                    <Label>From Ayah</Label>
                    <Input type="number" min="1" bind:value={form_state.ayah_start} data-testid="input-lesson-ayah-start" />
                </div>
                <div class="space-y-2">
                    <Label>To Ayah</Label>
                    <Input type="number" min="1" bind:value={form_state.ayah_end} data-testid="input-lesson-ayah-end" />
                </div>
            </div>

            <div class="space-y-2">
                <Label>Rating</Label>
                <div class="flex flex-wrap gap-2">
                    {#each rating_options as rating (rating)}
                        <Button
                            type="button"
                            size="sm"
                            variant={form_state.rating === rating ? 'default' : 'outline'}
                            onclick={() => (form_state.rating = rating)}
                            data-testid={`button-rating-${rating.toLowerCase().replace(' ', '-')}`}
                        >
                            {rating}
                        </Button>
                    {/each}
                </div>
            </div>

            <div class="flex items-center gap-3 rounded-md border p-3">
                <Switch bind:checked={form_state.extra_work} data-testid="switch-extra-work" />
                <div class="space-y-0.5">
                    <Label class="cursor-pointer">Extra Work</Label>
                    <p class="text-xs text-muted-foreground">Student completed additional work</p>
                </div>
            </div>

            <div class="space-y-2">
                <Label>Comments (Optional)</Label>
                <Textarea
                    class="resize-none"
                    rows="3"
                    bind:value={form_state.comments}
                    placeholder="Add any notes about this lesson..."
                    data-testid="textarea-lesson-comments"
                />
            </div>

            <Dialog.Footer>
                <Button type="submit" disabled={is_saving} data-testid="button-submit-lesson">
                    {is_saving ? 'Logging...' : 'Log Lesson'}
                </Button>
            </Dialog.Footer>
        </form>
    </Dialog.Content>
</Dialog.Root>

<script>
import CalendarIcon from '@lucide/svelte/icons/calendar'
import PlusIcon from '@lucide/svelte/icons/plus'
import {toast} from 'svelte-sonner'

import {api_get, api_request} from '$lib/api.js'
import DataTable from '$lib/components/data-table.svelte'
import PageHeader from '$lib/components/page-header.svelte'
import StatusBadge, {get_rating_status_type} from '$lib/components/status-badge.svelte'
import {format_date_input} from '$lib/date.js'
import {SURAH_NAMES} from '$lib/quran.js'
import {Button} from '$ui/button/index.js'
import * as Card from '$ui/card/index.js'
import * as Dialog from '$ui/dialog/index.js'
import {Input} from '$ui/input/index.js'
import {Label} from '$ui/label/index.js'
import * as Select from '$ui/select/index.js'
import {Switch} from '$ui/switch/index.js'
import * as Tabs from '$ui/tabs/index.js'
import {Textarea} from '$ui/textarea/index.js'

let lessons = $state([])
let students = $state([])
let is_loading = $state(true)
let is_saving = $state(false)

let is_form_open = $state(false)
let selected_date = $state(format_date_input(new Date()))
let filter_type = $state('ALL')

let form_state = $state({
    student_id: '',
    date: format_date_input(new Date()),
    lesson_type: 'NEW',
    juz: 1,
    surah: '',
    ayah_start: 1,
    ayah_end: 5,
    comments: '',
    rating: 'Pass',
    extra_work: false,
})

const lesson_type_labels = {
    NEW: 'New Lesson',
    FRONT_REVISION: 'Front Revision',
    MURAJAH: "Muraja'ah",
}

const lesson_type_options = [
    {value: 'NEW', label: 'New Lesson'},
    {value: 'FRONT_REVISION', label: 'Front Revision'},
    {value: 'MURAJAH', label: "Muraja'ah"},
]

const rating_options = ['Pass', 'Re-do', 'Absent', 'Not Ready']

const active_students = $derived(students.filter(student => student.status === 'active'))

const student_label = $derived(
    form_state.student_id
        ? active_students.find(student => student.id === form_state.student_id)?.name ?? 'Select student'
        : 'Select student',
)

const lesson_type_label = $derived(
    lesson_type_options.find(option => option.value === form_state.lesson_type)?.label ?? 'Select lesson type',
)

const surah_options = SURAH_NAMES.map((name, index) => ({
    value: name,
    label: `${index + 1}. ${name}`,
}))

const surah_label = $derived(
    surah_options.find(option => option.value === form_state.surah)?.label ?? 'Select surah',
)

const filtered_lessons = $derived(
    lessons.filter(lesson => filter_type === 'ALL' || lesson.lessonType === filter_type),
)

const lesson_counts = $derived({
    all: lessons.length,
    new: lessons.filter(lesson => lesson.lessonType === 'NEW').length,
    front: lessons.filter(lesson => lesson.lessonType === 'FRONT_REVISION').length,
    muraja: lessons.filter(lesson => lesson.lessonType === 'MURAJAH').length,
})

const columns = [
    {key: 'student', header: 'Student'},
    {key: 'lesson_type', header: 'Type'},
    {key: 'content', header: 'Content'},
    {key: 'juz', header: 'Juz'},
    {key: 'rating', header: 'Rating'},
    {key: 'extra', header: 'Extra'},
]

function row_key(lesson) {
    return lesson.id
}

function open_form() {
    form_state = {
        student_id: '',
        date: selected_date,
        lesson_type: 'NEW',
        juz: 1,
        surah: '',
        ayah_start: 1,
        ayah_end: 5,
        comments: '',
        rating: 'Pass',
        extra_work: false,
    }
    is_form_open = true
}

function handle_date_change() {
    form_state.date = selected_date
    load_lessons()
}

async function load_lessons() {
    is_loading = true
    lessons = (await api_get('/api/lessons', {date: selected_date})) ?? []
    is_loading = false
}

async function load_students() {
    students = (await api_get('/api/students')) ?? []
}

async function submit_form(event) {
    event.preventDefault()
    is_saving = true

    const payload = {
        studentId: form_state.student_id,
        date: form_state.date,
        lessonType: form_state.lesson_type,
        juz: Number(form_state.juz),
        surah: form_state.surah,
        ayahStart: Number(form_state.ayah_start),
        ayahEnd: Number(form_state.ayah_end),
        comments: form_state.comments || null,
        rating: form_state.rating,
        extraWork: form_state.extra_work,
    }

    const response = await api_request('POST', '/api/lessons', payload)
    if (response === false) {
        toast.error('Failed to log lesson')
        is_saving = false
        return
    }

    toast.success('Lesson logged successfully')
    is_form_open = false
    is_saving = false
    await load_lessons()
}

;(async () => {
    await load_students()
    await load_lessons()
})()
</script>
