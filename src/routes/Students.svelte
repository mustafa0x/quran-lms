{#snippet actions()}
    <Button onclick={open_add} data-testid="button-add-student">
        <PlusIcon class="mr-2 h-4 w-4" />
        Add Student
    </Button>
{/snippet}

<PageHeader
    title="Students"
    description="Manage your Quran memorization students"
    {actions}
/>

<div class="space-y-6">
    <div class="relative max-w-sm">
        <SearchIcon class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
            placeholder="Search students..."
            class="pl-9"
            bind:value={search_query}
            data-testid="input-search-students"
        />
    </div>

    <Card.Root>
        <Card.Header class="pb-3">
            <Card.Title class="text-base">Filters</Card.Title>
        </Card.Header>
        <Card.Content class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div class="space-y-2">
                <Label>Gender</Label>
                <Select.Root bind:value={filters.gender}>
                    <Select.Trigger data-testid="filter-student-gender">
                        <span data-slot="select-value">{filter_gender_label}</span>
                    </Select.Trigger>
                    <Select.Content>
                        {#each filter_gender_options as option (option.value)}
                            <Select.Item value={option.value}>{option.label}</Select.Item>
                        {/each}
                    </Select.Content>
                </Select.Root>
            </div>
            <div class="space-y-2">
                <Label>Status</Label>
                <Select.Root bind:value={filters.status}>
                    <Select.Trigger data-testid="filter-student-status">
                        <span data-slot="select-value">{filter_status_label}</span>
                    </Select.Trigger>
                    <Select.Content>
                        {#each filter_status_options as option (option.value)}
                            <Select.Item value={option.value}>{option.label}</Select.Item>
                        {/each}
                    </Select.Content>
                </Select.Root>
            </div>
            <div class="space-y-2">
                <Label>Teacher</Label>
                <Select.Root bind:value={filters.teacher_id}>
                    <Select.Trigger data-testid="filter-student-teacher">
                        <span data-slot="select-value">{filter_teacher_label}</span>
                    </Select.Trigger>
                    <Select.Content>
                        <Select.Item value="all">All teachers</Select.Item>
                        {#each teachers as teacher (teacher.id)}
                            <Select.Item value={teacher.id}>{teacher.name}</Select.Item>
                        {/each}
                    </Select.Content>
                </Select.Root>
            </div>
            <div class="space-y-2">
                <Label>Juz Range</Label>
                <div class="grid grid-cols-2 gap-2">
                    <Input
                        type="number"
                        min="0"
                        max="30"
                        placeholder="Min"
                        bind:value={filters.juz_min}
                        data-testid="filter-student-juz-min"
                    />
                    <Input
                        type="number"
                        min="0"
                        max="30"
                        placeholder="Max"
                        bind:value={filters.juz_max}
                        data-testid="filter-student-juz-max"
                    />
                </div>
            </div>
            <div class="space-y-2">
                <Label>Enrollment Dates</Label>
                <div class="grid grid-cols-2 gap-2">
                    <Input
                        type="date"
                        bind:value={filters.enrollment_start}
                        data-testid="filter-student-enrollment-start"
                    />
                    <Input
                        type="date"
                        bind:value={filters.enrollment_end}
                        data-testid="filter-student-enrollment-end"
                    />
                </div>
            </div>
            <div class="space-y-2">
                <Label>Age Range</Label>
                <div class="grid grid-cols-2 gap-2">
                    <Input
                        type="number"
                        min="1"
                        placeholder="Min"
                        bind:value={filters.age_min}
                        data-testid="filter-student-age-min"
                    />
                    <Input
                        type="number"
                        min="1"
                        placeholder="Max"
                        bind:value={filters.age_max}
                        data-testid="filter-student-age-max"
                    />
                </div>
            </div>
            <div class="flex items-end">
                <Button variant="outline" onclick={reset_filters} data-testid="button-reset-student-filters">
                    Reset Filters
                </Button>
            </div>
        </Card.Content>
    </Card.Root>

    {#snippet cell(student, column)}
        {#if column.key === 'name'}
            <div class="flex items-center gap-3">
                <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-sm font-medium text-primary">
                    {student.name.charAt(0).toUpperCase()}
                </div>
                <span class="font-medium">{student.name}</span>
            </div>
        {:else if column.key === 'gender'}
            <span class="capitalize">{student.gender}</span>
        {:else if column.key === 'current_juz'}
            Juz {student.currentJuz}
        {:else if column.key === 'progress'}
            <div class="flex items-center gap-2">
                <ProgressRing value={student.totalJuzMemorized} max={30} size={36} stroke_width={3} />
                <span class="text-sm text-muted-foreground">{student.totalJuzMemorized}/30</span>
            </div>
        {:else if column.key === 'teacher'}
            {student.teacher?.name ?? '-'}
        {:else if column.key === 'status'}
            <StatusBadge status={get_student_status_type(student.status)}>{student.status}</StatusBadge>
        {:else if column.key === 'actions'}
            <div class="flex items-center justify-end gap-1">
                <Button
                    variant="ghost"
                    size="icon"
                    onclick={() => open_view(student)}
                    data-testid={`button-view-student-${student.id}`}
                >
                    <EyeIcon class="h-4 w-4" />
                </Button>
                <Button
                    variant="ghost"
                    size="icon"
                    onclick={() => open_edit(student)}
                    data-testid={`button-edit-student-${student.id}`}
                >
                    <EditIcon class="h-4 w-4" />
                </Button>
                <Button
                    variant="ghost"
                    size="icon"
                    onclick={() => open_delete(student)}
                    data-testid={`button-delete-student-${student.id}`}
                >
                    <TrashIcon class="h-4 w-4 text-destructive" />
                </Button>
            </div>
        {/if}
    {/snippet}

    <DataTable
        {columns}
        data={filtered_students}
        {cell}
        get_row_key={row_key}
        test_id_prefix="students"
        is_loading={is_loading}
        empty_message="No students found. Add your first student to get started."
    />
</div>

<Dialog.Root bind:open={is_form_open}>
    <Dialog.Content class="max-w-lg">
        <Dialog.Header>
            <Dialog.Title>{editing_student ? 'Edit Student' : 'Add New Student'}</Dialog.Title>
        </Dialog.Header>
        <form class="space-y-4" onsubmit={submit_form}>
            <div class="space-y-2">
                <Label>Name</Label>
                <Input
                    placeholder="Enter student name"
                    bind:value={form_state.name}
                    data-testid="input-student-name"
                />
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                    <Label>Gender</Label>
                    <Select.Root bind:value={form_state.gender}>
                        <Select.Trigger data-testid="select-student-gender">
                            <span data-slot="select-value">{gender_label}</span>
                        </Select.Trigger>
                        <Select.Content>
                            {#each gender_options as option (option.value)}
                                <Select.Item value={option.value}>{option.label}</Select.Item>
                            {/each}
                        </Select.Content>
                    </Select.Root>
                </div>

                <div class="space-y-2">
                    <Label>Status</Label>
                    <Select.Root bind:value={form_state.status}>
                        <Select.Trigger data-testid="select-student-status">
                            <span data-slot="select-value">{status_label}</span>
                        </Select.Trigger>
                        <Select.Content>
                            {#each status_options as option (option.value)}
                                <Select.Item value={option.value}>{option.label}</Select.Item>
                            {/each}
                        </Select.Content>
                    </Select.Root>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                    <Label>Date of Birth</Label>
                    <Input type="date" bind:value={form_state.date_of_birth} data-testid="input-student-dob" />
                </div>
                <div class="space-y-2">
                    <Label>Enrollment Date</Label>
                    <Input
                        type="date"
                        bind:value={form_state.enrollment_date}
                        data-testid="input-student-enrollment"
                    />
                </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                    <Label>Current Juz</Label>
                    <Input
                        type="number"
                        min="1"
                        max="30"
                        bind:value={form_state.current_juz}
                        data-testid="input-student-current-juz"
                    />
                </div>
                <div class="space-y-2">
                    <Label>Total Juz Memorized</Label>
                    <Input
                        type="number"
                        min="0"
                        max="30"
                        bind:value={form_state.total_juz_memorized}
                        data-testid="input-student-total-juz"
                    />
                </div>
            </div>

            <div class="space-y-2">
                <Label>Assigned Teacher</Label>
                <Select.Root bind:value={form_state.teacher_id}>
                    <Select.Trigger data-testid="select-student-teacher">
                        <span data-slot="select-value">{teacher_label}</span>
                    </Select.Trigger>
                    <Select.Content>
                        <Select.Item value="">No teacher assigned</Select.Item>
                        {#each teachers as teacher (teacher.id)}
                            <Select.Item value={teacher.id}>{teacher.name}</Select.Item>
                        {/each}
                    </Select.Content>
                </Select.Root>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                    <Label>Goal Juz</Label>
                    <Input
                        type="number"
                        min="1"
                        max="30"
                        placeholder="Optional"
                        bind:value={form_state.goal_juz}
                        data-testid="input-student-goal-juz"
                    />
                </div>
                <div class="space-y-2">
                    <Label>Goal Date</Label>
                    <Input type="date" bind:value={form_state.goal_date} data-testid="input-student-goal-date" />
                </div>
            </div>

            <div class="space-y-2">
                <Label>Challenges</Label>
                <Textarea
                    rows="3"
                    placeholder="Notes about challenges or focus areas"
                    bind:value={form_state.challenges}
                    data-testid="textarea-student-challenges"
                />
            </div>

            <Dialog.Footer>
                <Button type="submit" disabled={is_saving} data-testid="button-submit-student">
                    {is_saving ? 'Saving...' : 'Save Student'}
                </Button>
            </Dialog.Footer>
        </form>
    </Dialog.Content>
</Dialog.Root>

<Dialog.Root bind:open={is_view_open}>
    <Dialog.Content class="max-w-lg">
        <Dialog.Header>
            <Dialog.Title>Student Details</Dialog.Title>
        </Dialog.Header>
        {#if viewing_student}
            <div class="space-y-6">
                <div class="flex items-center gap-4">
                    <div class="flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-2xl font-bold text-primary">
                        {viewing_student.name.charAt(0).toUpperCase()}
                    </div>
                    <div>
                        <h3 class="text-xl font-semibold">{viewing_student.name}</h3>
                        <p class="text-sm text-muted-foreground capitalize">{viewing_student.gender}</p>
                    </div>
                    <StatusBadge status={get_student_status_type(viewing_student.status)} test_id="status-student">
                        {viewing_student.status}
                    </StatusBadge>
                </div>

                <div class="flex justify-center">
                    <ProgressRing
                        value={viewing_student.totalJuzMemorized}
                        max={30}
                        size={140}
                        stroke_width={12}
                        label="of 30 Juz"
                    />
                </div>

                <Card.Root>
                    <Card.Header class="pb-3">
                        <Card.Title class="text-base">Details</Card.Title>
                    </Card.Header>
                    <Card.Content class="space-y-3 text-sm">
                        <div class="flex justify-between">
                            <span class="text-muted-foreground">Current Juz</span>
                            <span class="font-medium">Juz {viewing_student.currentJuz}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-muted-foreground">Total Memorized</span>
                            <span class="font-medium">{viewing_student.totalJuzMemorized} Juz</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-muted-foreground">Teacher</span>
                            <span class="font-medium">{viewing_student.teacher?.name ?? 'Not assigned'}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-muted-foreground">Enrolled</span>
                            <span class="font-medium">{viewing_student.enrollmentDate}</span>
                        </div>
                        {#if viewing_student.dateOfBirth}
                            <div class="flex justify-between">
                                <span class="text-muted-foreground">Date of Birth</span>
                                <span class="font-medium">{viewing_student.dateOfBirth}</span>
                            </div>
                        {/if}
                    </Card.Content>
                </Card.Root>

                <Card.Root>
                    <Card.Header class="pb-3">
                        <Card.Title class="text-base">Goals & Challenges</Card.Title>
                    </Card.Header>
                    <Card.Content class="space-y-3 text-sm">
                        <div class="flex justify-between">
                            <span class="text-muted-foreground">Goal</span>
                            <span class="font-medium">
                                {#if viewing_student.goalJuz}
                                    {viewing_student.goalJuz} Juz
                                    {#if viewing_student.goalDate}
                                        by {viewing_student.goalDate}
                                    {/if}
                                {:else}
                                    Not set
                                {/if}
                            </span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-muted-foreground">Challenges</span>
                            <span class="font-medium">{viewing_student.challenges ?? 'None noted'}</span>
                        </div>
                    </Card.Content>
                </Card.Root>

                <Card.Root>
                    <Card.Header class="pb-3">
                        <Card.Title class="text-base">Progress Report</Card.Title>
                    </Card.Header>
                    <Card.Content>
                        {#if is_report_loading}
                            <div class="space-y-3">
                                {#each Array.from({length: 3}) as _, index (index)}
                                    <Skeleton class="h-6 w-full" />
                                {/each}
                            </div>
                        {:else if student_report}
                            <div class="space-y-4 text-sm">
                                <div class="grid gap-3 sm:grid-cols-2">
                                    <div class="rounded-md border p-3">
                                        <p class="text-xs text-muted-foreground">Current Memorization</p>
                                        <p class="font-medium">
                                            Juz {student_report.currentMemorization.juz}
                                            {#if student_report.currentMemorization.surah}
                                                · {student_report.currentMemorization.surah}
                                            {/if}
                                            {#if student_report.currentMemorization.ayah}
                                                · Ayah {student_report.currentMemorization.ayah}
                                            {/if}
                                        </p>
                                    </div>
                                    <div class="rounded-md border p-3">
                                        <p class="text-xs text-muted-foreground">Totals</p>
                                        <p class="font-medium">
                                            {student_report.totals.totalJuz} Juz · {student_report.totals.totalSurahs} Surahs
                                            · {student_report.totals.totalAyahs} Ayahs
                                        </p>
                                    </div>
                                    <div class="rounded-md border p-3">
                                        <p class="text-xs text-muted-foreground">New Work (This Week)</p>
                                        <p class="font-medium">
                                            {student_report.newWork.thisWeekAyahs} Ayahs · {student_report.newWork.thisWeekSurahs} Surahs
                                        </p>
                                    </div>
                                    <div class="rounded-md border p-3">
                                        <p class="text-xs text-muted-foreground">Average Rate</p>
                                        <p class="font-medium">{student_report.newWork.averageAyahsPerWeek} Ayahs/week</p>
                                    </div>
                                </div>

                                <div class="grid gap-3 sm:grid-cols-2">
                                    <div class="rounded-md border p-3">
                                        <p class="text-xs text-muted-foreground">Last Revision</p>
                                        <p class="font-medium">{student_report.revision.lastRevisionDate ?? 'Not recorded'}</p>
                                    </div>
                                    <div class="rounded-md border p-3">
                                        <p class="text-xs text-muted-foreground">Next Revision Due</p>
                                        <p class="font-medium">{student_report.revision.nextRevisionDueDate ?? 'Not scheduled'}</p>
                                        {#if student_report.revision.murajaOnlyUntil}
                                            <p class="text-xs text-muted-foreground">Muraja only until {student_report.revision.murajaOnlyUntil}</p>
                                        {/if}
                                    </div>
                                </div>

                                <div class="grid gap-3 sm:grid-cols-2">
                                    <div class="rounded-md border p-3">
                                        <p class="text-xs text-muted-foreground">Homework (Last 30 Days)</p>
                                        {#if student_report.homework.totalCount > 0}
                                            <p class="font-medium">{student_report.homework.passRate}% pass rate</p>
                                            <p class="text-xs text-muted-foreground">
                                                {student_report.homework.passedCount} passed · {student_report.homework.failedCount} missed
                                            </p>
                                        {:else}
                                            <p class="font-medium">No homework records</p>
                                        {/if}
                                    </div>
                                    <div class="rounded-md border p-3">
                                        <p class="text-xs text-muted-foreground">Recent Ratings</p>
                                        {#if student_report.recentRatings.length > 0}
                                            <div class="mt-2 space-y-1 text-xs">
                                                {#each student_report.recentRatings as rating (rating.date + rating.lessonType + rating.surah)}
                                                    <div class="flex items-center justify-between">
                                                        <span>{rating.date} · {format_lesson_type(rating.lessonType)}</span>
                                                        <StatusBadge status={get_rating_status_type(rating.rating)}>{rating.rating}</StatusBadge>
                                                    </div>
                                                {/each}
                                            </div>
                                        {:else}
                                            <p class="font-medium">No recent ratings</p>
                                        {/if}
                                    </div>
                                </div>

                                <div class="space-y-2">
                                    <p class="text-xs text-muted-foreground">Weekly Trend</p>
                                    <div class="space-y-2">
                                        {#each student_report.performanceTrend as trend (trend.weekStart)}
                                            <div class="flex items-center gap-3">
                                                <span class="w-20 text-xs text-muted-foreground">{trend.weekStart}</span>
                                                <div class="h-2 flex-1 rounded-full bg-muted">
                                                    <div
                                                        class="h-2 rounded-full bg-primary"
                                                        style="width: {get_trend_width(trend.ayahs)}%"
                                                    ></div>
                                                </div>
                                                <span class="text-xs font-medium">{trend.ayahs}</span>
                                            </div>
                                        {/each}
                                    </div>
                                </div>

                                <div class="space-y-2">
                                    <p class="text-xs text-muted-foreground">Recent Assessments</p>
                                    {#if student_report.assessments.length > 0}
                                        <div class="space-y-2">
                                            {#each student_report.assessments as assessment (assessment.id)}
                                                <div class="flex items-center justify-between rounded-md border p-2">
                                                    <div>
                                                        <p class="font-medium">{assessment.type} · {assessment.score}</p>
                                                        <p class="text-xs text-muted-foreground">{assessment.date}</p>
                                                    </div>
                                                    <span class="text-xs text-muted-foreground">{assessment.notes ?? 'No notes'}</span>
                                                </div>
                                            {/each}
                                        </div>
                                    {:else}
                                        <p class="text-xs text-muted-foreground">No assessments yet</p>
                                    {/if}
                                    <div class="mt-3 space-y-2">
                                        <p class="text-xs text-muted-foreground">Log Assessment</p>
                                        <div class="grid gap-2 sm:grid-cols-2">
                                            <Input type="date" bind:value={assessment_form.date} data-testid="input-assessment-date" />
                                            <Select.Root bind:value={assessment_form.type}>
                                                <Select.Trigger data-testid="select-assessment-type">
                                                    <span data-slot="select-value">{assessment_type_label}</span>
                                                </Select.Trigger>
                                                <Select.Content>
                                                    {#each assessment_type_options as option (option.value)}
                                                        <Select.Item value={option.value}>{option.label}</Select.Item>
                                                    {/each}
                                                </Select.Content>
                                            </Select.Root>
                                            <Input
                                                type="number"
                                                min="0"
                                                max="100"
                                                placeholder="Score"
                                                bind:value={assessment_form.score}
                                                data-testid="input-assessment-score"
                                            />
                                            <Input
                                                placeholder="Notes (optional)"
                                                bind:value={assessment_form.notes}
                                                data-testid="input-assessment-notes"
                                            />
                                        </div>
                                        <Button
                                            size="sm"
                                            disabled={is_assessment_saving || !assessment_form.score}
                                            onclick={submit_assessment}
                                            data-testid="button-save-assessment"
                                        >
                                            {is_assessment_saving ? 'Saving...' : 'Save Assessment'}
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        {:else}
                            <p class="text-sm text-muted-foreground">Unable to load report data.</p>
                        {/if}
                    </Card.Content>
                </Card.Root>
            </div>
        {/if}
    </Dialog.Content>
</Dialog.Root>

<AlertDialog.Root bind:open={is_delete_open}>
    <AlertDialog.Content>
        <AlertDialog.Header>
            <AlertDialog.Title>Delete Student</AlertDialog.Title>
            <AlertDialog.Description>
                Are you sure you want to delete {deleting_student?.name}? This action cannot be undone.
            </AlertDialog.Description>
        </AlertDialog.Header>
        <AlertDialog.Footer>
            <AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
            <AlertDialog.Action
                class="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                onclick={confirm_delete}
            >
                Delete
            </AlertDialog.Action>
        </AlertDialog.Footer>
    </AlertDialog.Content>
</AlertDialog.Root>

<script>
import EditIcon from '@lucide/svelte/icons/edit-2'
import EyeIcon from '@lucide/svelte/icons/eye'
import PlusIcon from '@lucide/svelte/icons/plus'
import SearchIcon from '@lucide/svelte/icons/search'
import TrashIcon from '@lucide/svelte/icons/trash-2'

import {toast} from 'svelte-sonner'

import {api_get, api_request} from '$lib/api.js'
import {format_date_input} from '$lib/date.js'
import * as AlertDialog from '$ui/alert-dialog/index.js'
import {Button} from '$ui/button/index.js'
import * as Card from '$ui/card/index.js'
import * as Dialog from '$ui/dialog/index.js'
import {Input} from '$ui/input/index.js'
import {Label} from '$ui/label/index.js'
import * as Select from '$ui/select/index.js'
import {Skeleton} from '$ui/skeleton/index.js'
import {Textarea} from '$ui/textarea/index.js'
import DataTable from '$lib/components/data-table.svelte'
import PageHeader from '$lib/components/page-header.svelte'
import ProgressRing from '$lib/components/progress-ring.svelte'
import StatusBadge, {get_rating_status_type, get_student_status_type} from '$lib/components/status-badge.svelte'

let students = $state([])
let teachers = $state([])
let is_loading = $state(true)
let is_saving = $state(false)

let search_query = $state('')

let is_form_open = $state(false)
let is_view_open = $state(false)
let is_delete_open = $state(false)

let editing_student = $state(null)
let viewing_student = $state(null)
let deleting_student = $state(null)
let student_report = $state(null)
let is_report_loading = $state(false)
let assessment_form = $state({
    date: format_date_input(new Date()),
    type: 'Test',
    score: '',
    notes: '',
})
let is_assessment_saving = $state(false)

let filters = $state({
    gender: 'all',
    status: 'all',
    teacher_id: 'all',
    juz_min: '',
    juz_max: '',
    enrollment_start: '',
    enrollment_end: '',
    age_min: '',
    age_max: '',
})

let form_state = $state({
    name: '',
    gender: 'male',
    date_of_birth: '',
    enrollment_date: format_date_input(new Date()),
    current_juz: 1,
    total_juz_memorized: 0,
    goal_juz: '',
    goal_date: '',
    challenges: '',
    teacher_id: '',
    status: 'active',
})

const gender_options = [
    {value: 'male', label: 'Male'},
    {value: 'female', label: 'Female'},
]

const status_options = [
    {value: 'active', label: 'Active'},
    {value: 'inactive', label: 'Inactive'},
]

const filter_gender_options = [
    {value: 'all', label: 'All genders'},
    ...gender_options,
]

const filter_status_options = [
    {value: 'all', label: 'All statuses'},
    ...status_options,
]

const assessment_type_options = [
    {value: 'Test', label: 'Test'},
    {value: 'Quarterly', label: 'Quarterly'},
]

const lesson_type_labels = {
    NEW: 'New',
    FRONT_REVISION: 'Front Revision',
    MURAJAH: "Muraja'ah",
}

const gender_label = $derived(gender_options.find(option => option.value === form_state.gender)?.label ?? 'Select')
const status_label = $derived(status_options.find(option => option.value === form_state.status)?.label ?? 'Select')
const teacher_label = $derived(
    form_state.teacher_id
        ? teachers.find(teacher => teacher.id === form_state.teacher_id)?.name ?? 'Select teacher'
        : 'No teacher assigned',
)

const filter_gender_label = $derived(
    filter_gender_options.find(option => option.value === filters.gender)?.label ?? 'All genders',
)
const filter_status_label = $derived(
    filter_status_options.find(option => option.value === filters.status)?.label ?? 'All statuses',
)
const filter_teacher_label = $derived(
    filters.teacher_id !== 'all'
        ? teachers.find(teacher => teacher.id === filters.teacher_id)?.name ?? 'All teachers'
        : 'All teachers',
)

const assessment_type_label = $derived(
    assessment_type_options.find(option => option.value === assessment_form.type)?.label ?? 'Select type',
)

const filtered_students = $derived(
    students.filter(student => {
        const matches_search = student.name.toLowerCase().includes(search_query.toLowerCase())
        if (!matches_search) return false
        if (filters.gender !== 'all' && student.gender !== filters.gender) return false
        if (filters.status !== 'all' && student.status !== filters.status) return false
        if (filters.teacher_id !== 'all' && student.teacherId !== filters.teacher_id) return false

        if (filters.juz_min && Number(student.totalJuzMemorized) < Number(filters.juz_min)) return false
        if (filters.juz_max && Number(student.totalJuzMemorized) > Number(filters.juz_max)) return false

        if (filters.enrollment_start && student.enrollmentDate < filters.enrollment_start) return false
        if (filters.enrollment_end && student.enrollmentDate > filters.enrollment_end) return false

        const age = get_student_age(student.dateOfBirth)
        if (filters.age_min && age !== null && age < Number(filters.age_min)) return false
        if (filters.age_max && age !== null && age > Number(filters.age_max)) return false

        return true
    }),
)

const columns = [
    {key: 'name', header: 'Name'},
    {key: 'gender', header: 'Gender'},
    {key: 'current_juz', header: 'Current Juz'},
    {key: 'progress', header: 'Progress'},
    {key: 'teacher', header: 'Teacher'},
    {key: 'status', header: 'Status'},
    {key: 'actions', header: '', class_name: 'text-right'},
]

function row_key(student) {
    return student.id
}

function format_lesson_type(value) {
    return lesson_type_labels[value] ?? value
}

function get_student_age(date_value) {
    if (!date_value) return null
    const birth = new Date(date_value)
    if (Number.isNaN(birth.getTime())) return null
    const today = new Date()
    let age = today.getFullYear() - birth.getFullYear()
    const month_gap = today.getMonth() - birth.getMonth()
    if (month_gap < 0 || (month_gap === 0 && today.getDate() < birth.getDate())) age -= 1
    return age
}

function reset_form_state(student = null) {
    if (student) {
        form_state = {
            name: student.name,
            gender: student.gender,
            date_of_birth: student.dateOfBirth ?? '',
            enrollment_date: student.enrollmentDate,
            current_juz: student.currentJuz,
            total_juz_memorized: student.totalJuzMemorized,
            goal_juz: student.goalJuz ?? '',
            goal_date: student.goalDate ?? '',
            challenges: student.challenges ?? '',
            teacher_id: student.teacherId ?? '',
            status: student.status,
        }
        return
    }

    form_state = {
        name: '',
        gender: 'male',
        date_of_birth: '',
        enrollment_date: format_date_input(new Date()),
        current_juz: 1,
        total_juz_memorized: 0,
        goal_juz: '',
        goal_date: '',
        challenges: '',
        teacher_id: '',
        status: 'active',
    }
}

function open_add() {
    editing_student = null
    reset_form_state()
    is_form_open = true
}

function open_edit(student) {
    editing_student = student
    reset_form_state(student)
    is_form_open = true
}

function open_view(student) {
    viewing_student = student
    is_view_open = true
    assessment_form = {
        date: format_date_input(new Date()),
        type: 'Test',
        score: '',
        notes: '',
    }
    load_student_report(student.id)
}

function open_delete(student) {
    deleting_student = student
    is_delete_open = true
}

async function load_students() {
    is_loading = true
    students = (await api_get('/api/students')) ?? []
    is_loading = false
}

async function load_teachers() {
    teachers = (await api_get('/api/teachers')) ?? []
}

async function submit_form(event) {
    event.preventDefault()
    is_saving = true

    const payload = {
        name: form_state.name.trim(),
        gender: form_state.gender,
        dateOfBirth: form_state.date_of_birth || null,
        enrollmentDate: form_state.enrollment_date,
        currentJuz: Number(form_state.current_juz),
        totalJuzMemorized: Number(form_state.total_juz_memorized),
        goalJuz: form_state.goal_juz ? Number(form_state.goal_juz) : null,
        goalDate: form_state.goal_date || null,
        challenges: form_state.challenges || null,
        teacherId: form_state.teacher_id || null,
        status: form_state.status,
    }

    const response = editing_student
        ? await api_request('PATCH', `/api/students/${editing_student.id}`, payload)
        : await api_request('POST', '/api/students', payload)

    if (response === false) {
        toast.error(editing_student ? 'Failed to update student' : 'Failed to add student')
        is_saving = false
        return
    }

    toast.success(editing_student ? 'Student updated successfully' : 'Student added successfully')
    is_form_open = false
    editing_student = null
    is_saving = false
    await load_students()
}

async function confirm_delete() {
    if (!deleting_student) return
    const response = await api_request('DELETE', `/api/students/${deleting_student.id}`)
    if (response === false) {
        toast.error('Failed to delete student')
        return
    }
    toast.success('Student deleted successfully')
    is_delete_open = false
    deleting_student = null
    await load_students()
}

function reset_filters() {
    filters = {
        gender: 'all',
        status: 'all',
        teacher_id: 'all',
        juz_min: '',
        juz_max: '',
        enrollment_start: '',
        enrollment_end: '',
        age_min: '',
        age_max: '',
    }
}

function get_trend_width(ayahs) {
    if (!student_report?.performanceTrend?.length) return 0
    const max_value = Math.max(...student_report.performanceTrend.map(item => item.ayahs))
    if (!max_value) return 0
    return Math.round((ayahs / max_value) * 100)
}

async function load_student_report(student_id) {
    is_report_loading = true
    student_report = await api_get(`/api/reports/student/${student_id}`)
    is_report_loading = false
}

async function submit_assessment() {
    if (!viewing_student) return
    is_assessment_saving = true
    const payload = {
        studentId: viewing_student.id,
        date: assessment_form.date,
        type: assessment_form.type,
        score: Number(assessment_form.score),
        notes: assessment_form.notes || null,
    }
    const response = await api_request('POST', '/api/assessments', payload)
    if (response === false) {
        toast.error('Failed to save assessment')
        is_assessment_saving = false
        return
    }
    assessment_form = {
        date: format_date_input(new Date()),
        type: 'Test',
        score: '',
        notes: '',
    }
    is_assessment_saving = false
    await load_student_report(viewing_student.id)
}

;(async () => {
    await load_teachers()
    await load_students()
})()
</script>
