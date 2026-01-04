{#snippet actions()}
    <Button variant="outline" onclick={export_reports} data-testid="button-export-reports">
        <DownloadIcon class="mr-2 h-4 w-4" />
        Export
    </Button>
{/snippet}

<PageHeader
    title="Reports"
    description="View comprehensive program reports and analytics"
    {actions}
/>

<div class="space-y-6">
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card.Root>
            <Card.Content class="p-6">
                <div class="flex items-center gap-4">
                    <UsersIcon class="h-8 w-8 text-primary" />
                    <div>
                        <p class="text-sm text-muted-foreground">Total Students</p>
                        <p class="text-3xl font-bold">{stats?.totalStudents ?? 0}</p>
                    </div>
                </div>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-6">
                <div class="flex items-center gap-4">
                    <BookOpenIcon class="h-8 w-8 text-primary" />
                    <div>
                        <p class="text-sm text-muted-foreground">Total Juz Memorized</p>
                        <p class="text-3xl font-bold">{stats?.totalJuzMemorized ?? 0}</p>
                        <p class="text-xs text-muted-foreground">
                            {stats?.totalAyahsMemorized ?? 0} ayahs · {stats?.totalSurahsMemorized ?? 0} surahs
                        </p>
                    </div>
                </div>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-6">
                <div class="flex items-center gap-4">
                    <TrendingUpIcon class="h-8 w-8 text-primary" />
                    <div>
                        <p class="text-sm text-muted-foreground">Avg. Rate</p>
                        <p class="text-3xl font-bold">{stats?.averageMemorizationRate ?? 0}</p>
                        <p class="text-xs text-muted-foreground">ayahs/week</p>
                    </div>
                </div>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-6">
                <div class="flex items-center gap-4">
                    <AwardIcon class="h-8 w-8 text-primary" />
                    <div>
                        <p class="text-sm text-muted-foreground">Hafiz (30 Juz)</p>
                        <p class="text-3xl font-bold">{milestone_data.completed30}</p>
                    </div>
                </div>
            </Card.Content>
        </Card.Root>
    </div>

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <Card.Root>
            <Card.Content class="p-6">
                <p class="text-sm text-muted-foreground">Average Juz per Student</p>
                <p class="text-3xl font-bold">{average_juz}</p>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-6">
                <p class="text-sm text-muted-foreground">Retention Rate</p>
                <p class="text-3xl font-bold">{retention_rate}%</p>
                <p class="text-xs text-muted-foreground">On-track muraja schedules</p>
            </Card.Content>
        </Card.Root>
        <Card.Root>
            <Card.Content class="p-6">
                <p class="text-sm text-muted-foreground">Avg Completion Time</p>
                <p class="text-3xl font-bold">{average_completion_label}</p>
                <p class="text-xs text-muted-foreground">For students at 30 Juz</p>
            </Card.Content>
        </Card.Root>
    </div>

    <Tabs.Root bind:value={active_tab}>
        <Tabs.List>
            <Tabs.Trigger value="milestones" data-testid="tab-milestones">
                <AwardIcon class="mr-2 h-4 w-4" />
                Milestones
            </Tabs.Trigger>
            <Tabs.Trigger value="top" data-testid="tab-top-memorizers">
                <TrendingUpIcon class="mr-2 h-4 w-4" />
                Top Memorizers
            </Tabs.Trigger>
            <Tabs.Trigger value="distribution" data-testid="tab-distribution">
                <FileTextIcon class="mr-2 h-4 w-4" />
                Distribution
            </Tabs.Trigger>
        </Tabs.List>

        <Tabs.Content value="milestones" class="mt-6 space-y-6">
            <Card.Root>
                <Card.Header>
                    <Card.Title>Memorization Milestones</Card.Title>
                </Card.Header>
                <Card.Content>
                    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                        {#each milestone_cards as milestone (milestone.label)}
                            <div class="flex items-center justify-between rounded-lg border p-4">
                                <div class="flex items-center gap-3">
                                    <div class="h-3 w-3 rounded-full {milestone.color}"></div>
                                    <span class="font-medium">{milestone.label}</span>
                                </div>
                                <span class="text-2xl font-bold">{milestone.count}</span>
                            </div>
                        {/each}
                    </div>
                </Card.Content>
            </Card.Root>

            <Card.Root>
                <Card.Header>
                    <Card.Title>Juz Milestone Lists</Card.Title>
                </Card.Header>
                <Card.Content class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    {#each milestone_steps as step (step)}
                        {@const entries = milestone_report.juzMilestones?.[String(step)] ?? []}
                        <div class="rounded-md border p-4">
                            <p class="text-sm font-semibold">{step} Juz+</p>
                            {#if entries.length > 0}
                                <div class="mt-2 space-y-1 text-sm">
                                    {#each entries as student (student.id)}
                                        <div class="flex items-center justify-between">
                                            <span>{student.name}</span>
                                            <span class="text-muted-foreground">{student.totalJuzMemorized} Juz</span>
                                        </div>
                                    {/each}
                                </div>
                            {:else}
                                <p class="mt-2 text-sm text-muted-foreground">No students yet</p>
                            {/if}
                        </div>
                    {/each}
                </Card.Content>
            </Card.Root>

            <div class="grid gap-4 lg:grid-cols-2">
                <Card.Root>
                    <Card.Header>
                        <Card.Title>Percent Milestones</Card.Title>
                    </Card.Header>
                    <Card.Content class="space-y-3">
                        {#each percent_steps as step (step)}
                            {@const entries = milestone_report.percentMilestones?.[String(step)] ?? []}
                            <div class="rounded-md border p-3">
                                <p class="text-sm font-medium">{step}%+</p>
                                <p class="text-xs text-muted-foreground">
                                    {entries.length} students
                                </p>
                            </div>
                        {/each}
                    </Card.Content>
                </Card.Root>

                <Card.Root>
                    <Card.Header>
                        <Card.Title>Surah Milestones</Card.Title>
                    </Card.Header>
                    <Card.Content class="space-y-3">
                        {#each surah_steps as step (step)}
                            {@const entries = milestone_report.surahMilestones?.[String(step)] ?? []}
                            <div class="rounded-md border p-3">
                                <p class="text-sm font-medium">{step} Surahs+</p>
                                <p class="text-xs text-muted-foreground">
                                    {entries.length} students
                                </p>
                            </div>
                        {/each}
                    </Card.Content>
                </Card.Root>
            </div>
        </Tabs.Content>

        <Tabs.Content value="top" class="mt-6">
            <Card.Root>
                <Card.Header>
                    <Card.Title>Top 10 Memorizers (Last 30 Days)</Card.Title>
                </Card.Header>
                <Card.Content>
                    {#snippet top_cell(item, column)}
                        {#if column.key === 'student'}
                            <div class="flex items-center gap-3">
                                <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-sm font-medium text-primary">
                                    {item.student.name.charAt(0).toUpperCase()}
                                </div>
                                <span class="font-medium">{item.student.name}</span>
                            </div>
                        {:else if column.key === 'new_ayahs'}
                            <span class="font-medium">{item.newAyahs}</span>
                        {:else if column.key === 'new_surahs'}
                            <span class="font-medium">{item.newSurahs}</span>
                        {:else if column.key === 'lessons'}
                            <span class="font-medium">{item.lessonCount}</span>
                        {/if}
                    {/snippet}

                    <DataTable
                        columns={top_columns}
                        data={top_memorizers}
                        cell={top_cell}
                        get_row_key={top_row_key}
                        test_id_prefix="top-memorizers"
                        is_loading={is_loading}
                        empty_message="No students to display"
                    />
                </Card.Content>
            </Card.Root>
        </Tabs.Content>

        <Tabs.Content value="distribution" class="mt-6">
            <Card.Root>
                <Card.Header>
                    <Card.Title>Students by Juz Range</Card.Title>
                </Card.Header>
                <Card.Content>
                    <div class="space-y-4">
                        {#each Object.entries(students_by_juz) as [range, count] (range)}
                            {@const percentage = students.length > 0 ? Math.round((count / students.length) * 100) : 0}
                            <div class="space-y-2">
                                <div class="flex items-center justify-between text-sm">
                                    <span class="font-medium">{range} Juz</span>
                                    <span class="text-muted-foreground">
                                        {count} students ({percentage}%)
                                    </span>
                                </div>
                                <div class="h-3 rounded-full bg-muted">
                                    <div class="h-full rounded-full bg-primary transition-all" style="width: {percentage}%"></div>
                                </div>
                            </div>
                        {/each}
                    </div>
                </Card.Content>
            </Card.Root>
        </Tabs.Content>
    </Tabs.Root>

    <Card.Root>
        <Card.Header>
            <Card.Title>Revision Status</Card.Title>
        </Card.Header>
        <Card.Content class="space-y-4">
            <div class="grid gap-4 lg:grid-cols-3">
            <div class="rounded-md border p-4">
                <p class="text-sm font-semibold">Overdue</p>
                {#if revision_report.overdue.length > 0}
                    <div class="mt-2 space-y-2 text-sm">
                        {#each revision_report.overdue as schedule (schedule.id)}
                            <div class="flex items-center justify-between">
                                <span>{schedule.student?.name ?? 'Unknown'}</span>
                                <span class="text-muted-foreground">{schedule.nextRevisionDueDate ?? 'N/A'}</span>
                            </div>
                        {/each}
                    </div>
                {:else}
                    <p class="mt-2 text-sm text-muted-foreground">No overdue revisions</p>
                {/if}
            </div>
            <div class="rounded-md border p-4">
                <p class="text-sm font-semibold">Due Today</p>
                {#if revision_report.due.length > 0}
                    <div class="mt-2 space-y-2 text-sm">
                        {#each revision_report.due as schedule (schedule.id)}
                            <div class="flex items-center justify-between">
                                <span>{schedule.student?.name ?? 'Unknown'}</span>
                                <span class="text-muted-foreground">{schedule.nextRevisionDueDate ?? 'Today'}</span>
                            </div>
                        {/each}
                    </div>
                {:else}
                    <p class="mt-2 text-sm text-muted-foreground">No revisions due today</p>
                {/if}
            </div>
            <div class="rounded-md border p-4">
                <p class="text-sm font-semibold">Recently Completed</p>
                {#if revision_report.recentlyCompleted.length > 0}
                    <div class="mt-2 space-y-2 text-sm">
                        {#each revision_report.recentlyCompleted as schedule (schedule.id)}
                            <div class="flex items-center justify-between">
                                <span>{schedule.student?.name ?? 'Unknown'}</span>
                                <span class="text-muted-foreground">{schedule.lastCompletedDate ?? 'Completed'}</span>
                            </div>
                        {/each}
                    </div>
                {:else}
                    <p class="mt-2 text-sm text-muted-foreground">No recent completions</p>
                {/if}
            </div>
            </div>
            <div class="rounded-md border p-4">
                <p class="text-sm font-semibold">Muraja Only Periods</p>
                {#if revision_report.murajaOnly.length > 0}
                    <div class="mt-2 space-y-2 text-sm">
                        {#each revision_report.murajaOnly as student (student.id)}
                            <div class="flex items-center justify-between">
                                <span>{student.name}</span>
                                <span class="text-muted-foreground">{student.murajaOnlyUntil ?? ''}</span>
                            </div>
                        {/each}
                    </div>
                {:else}
                    <p class="mt-2 text-sm text-muted-foreground">No muraja-only periods</p>
                {/if}
            </div>
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Header>
            <Card.Title>Teacher Workload (Last 30 Days)</Card.Title>
        </Card.Header>
        <Card.Content>
            {#snippet teacher_cell(item, column)}
                {#if column.key === 'teacher'}
                    <span class="font-medium">{item.teacher.name}</span>
                {:else if column.key === 'students'}
                    <span class="font-medium">{item.studentCount}</span>
                {:else if column.key === 'lessons'}
                    <span class="font-medium">{item.lessonCount}</span>
                {:else if column.key === 'ayahs'}
                    <span class="font-medium">{item.totalAyahs}</span>
                {:else if column.key === 'surahs'}
                    <span class="font-medium">{item.totalSurahs}</span>
                {:else if column.key === 'assessments'}
                    <span class="font-medium">{item.upcomingAssessments}</span>
                {/if}
            {/snippet}

            <DataTable
                columns={teacher_columns}
                data={teacher_workload}
                cell={teacher_cell}
                get_row_key={teacher_row_key}
                test_id_prefix="teacher-workload"
                is_loading={is_loading}
                empty_message="No teacher data available"
            />
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Header>
            <Card.Title>Attendance Report (Last 30 Days)</Card.Title>
        </Card.Header>
        <Card.Content>
            {#snippet attendance_cell(item, column)}
                {#if column.key === 'student'}
                    <span class="font-medium">{item.student.name}</span>
                {:else if column.key === 'present'}
                    <span class="font-medium">{item.presentCount}</span>
                {:else if column.key === 'absent'}
                    <span class="font-medium">{item.absentCount}</span>
                {:else if column.key === 'rate'}
                    <span class="font-medium">{item.attendanceRate}%</span>
                {/if}
            {/snippet}

            <DataTable
                columns={attendance_columns}
                data={attendance_report}
                cell={attendance_cell}
                get_row_key={attendance_row_key}
                test_id_prefix="attendance-report"
                is_loading={is_loading}
                empty_message="No attendance data available"
            />
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Header>
            <Card.Title>Homework Report (Last 30 Days)</Card.Title>
        </Card.Header>
        <Card.Content>
            {#snippet homework_cell(item, column)}
                {#if column.key === 'student'}
                    <span class="font-medium">{item.student.name}</span>
                {:else if column.key === 'passed'}
                    <span class="font-medium">{item.passedCount}</span>
                {:else if column.key === 'failed'}
                    <span class="font-medium">{item.failedCount}</span>
                {:else if column.key === 'rate'}
                    <span class="font-medium">{item.passRate}%</span>
                {/if}
            {/snippet}

            <DataTable
                columns={homework_columns}
                data={homework_report}
                cell={homework_cell}
                get_row_key={homework_row_key}
                test_id_prefix="homework-report"
                is_loading={is_loading}
                empty_message="No homework data available"
            />
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Header>
            <Card.Title>Assessment Results</Card.Title>
        </Card.Header>
        <Card.Content class="space-y-4">
            <div class="rounded-md border p-3">
                <p class="text-xs text-muted-foreground">Overall Average</p>
                <p class="text-lg font-semibold">{assessments_report.averageScore}</p>
            </div>

            {#snippet assessment_cell(item, column)}
                {#if column.key === 'student'}
                    <span class="font-medium">{item.student.name}</span>
                {:else if column.key === 'average'}
                    <span class="font-medium">{item.averageScore}</span>
                {:else if column.key === 'last'}
                    <span class="font-medium">{item.lastScore}</span>
                {:else if column.key === 'date'}
                    <span class="font-medium">{item.lastDate}</span>
                {:else if column.key === 'type'}
                    <span class="font-medium">{item.lastType}</span>
                {/if}
            {/snippet}

            <DataTable
                columns={assessment_columns}
                data={assessments_report.items}
                cell={assessment_cell}
                get_row_key={assessment_row_key}
                test_id_prefix="assessment-report"
                is_loading={is_loading}
                empty_message="No assessment data available"
            />
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Header>
            <Card.Title>Goals vs Actual</Card.Title>
        </Card.Header>
        <Card.Content>
            {#snippet goal_cell(item, column)}
                {#if column.key === 'student'}
                    <span class="font-medium">{item.student.name}</span>
                {:else if column.key === 'goal'}
                    <span class="font-medium">{item.goalJuz} Juz</span>
                {:else if column.key === 'progress'}
                    <span class="font-medium">{item.progressPercent}%</span>
                {:else if column.key === 'status'}
                    <StatusBadge status={item.status === 'met' ? 'success' : item.status === 'overdue' ? 'error' : 'warning'}>
                        {item.status.replace('_', ' ')}
                    </StatusBadge>
                {/if}
            {/snippet}

            <DataTable
                columns={goal_columns}
                data={goals_report}
                cell={goal_cell}
                get_row_key={goal_row_key}
                test_id_prefix="goal-report"
                is_loading={is_loading}
                empty_message="No goals set yet"
            />
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Header>
            <Card.Title>Struggling Students</Card.Title>
        </Card.Header>
        <Card.Content>
            {#if struggling_students.length > 0}
                <div class="space-y-3">
                    {#each struggling_students as entry (entry.student.id)}
                        <div class="rounded-md border p-3">
                            <div class="flex items-center justify-between">
                                <span class="font-medium">{entry.student.name}</span>
                                <span class="text-xs text-muted-foreground">{entry.averageAyahsPerWeek} ayahs/week</span>
                            </div>
                            <div class="mt-2 flex flex-wrap gap-2 text-xs text-muted-foreground">
                                {#each entry.reasons as reason (reason)}
                                    <span class="rounded-full bg-muted px-2 py-1">{reason}</span>
                                {/each}
                            </div>
                        </div>
                    {/each}
                </div>
            {:else}
                <p class="text-sm text-muted-foreground">No struggling students detected</p>
            {/if}
        </Card.Content>
    </Card.Root>
</div>

<script>
import AwardIcon from '@lucide/svelte/icons/award'
import BookOpenIcon from '@lucide/svelte/icons/book-open'
import DownloadIcon from '@lucide/svelte/icons/download'
import FileTextIcon from '@lucide/svelte/icons/file-text'
import TrendingUpIcon from '@lucide/svelte/icons/trending-up'
import UsersIcon from '@lucide/svelte/icons/users'

import {api_get} from '$lib/api.js'
import DataTable from '$lib/components/data-table.svelte'
import PageHeader from '$lib/components/page-header.svelte'
import StatusBadge from '$lib/components/status-badge.svelte'
import {Button} from '$ui/button/index.js'
import * as Card from '$ui/card/index.js'
import * as Tabs from '$ui/tabs/index.js'

let stats = $state(null)
let students = $state([])
let is_loading = $state(true)
let active_tab = $state('milestones')
let milestone_report = $state({juzMilestones: {}, percentMilestones: {}, surahMilestones: {}})
let top_memorizers = $state([])
let revision_report = $state({overdue: [], due: [], recentlyCompleted: [], murajaOnly: []})
let teacher_workload = $state([])
let attendance_report = $state([])
let homework_report = $state([])
let assessments_report = $state({averageScore: 0, items: []})
let goals_report = $state([])
let struggling_students = $state([])

const average_juz = $derived(
    students.length > 0
        ? Math.round((students.reduce((sum, student) => sum + student.totalJuzMemorized, 0) / students.length) * 10) / 10
        : 0,
)

const retention_rate = $derived(
    stats?.retentionRate ?? (
        stats?.activeStudents
            ? Math.round(((stats.activeStudents - stats.studentsOverdueMuraja) / stats.activeStudents) * 100)
            : 0
    ),
)

const average_completion_label = $derived(
    stats?.averageCompletionDays
        ? `${Math.round(stats.averageCompletionDays / 30)} months`
        : 'N/A',
)

const milestone_data = $derived({
    completed5: students.filter(student => student.totalJuzMemorized >= 5).length,
    completed10: students.filter(student => student.totalJuzMemorized >= 10).length,
    completed15: students.filter(student => student.totalJuzMemorized >= 15).length,
    completed20: students.filter(student => student.totalJuzMemorized >= 20).length,
    completed25: students.filter(student => student.totalJuzMemorized >= 25).length,
    completed30: students.filter(student => student.totalJuzMemorized >= 30).length,
})

const milestone_cards = $derived([
    {label: '5 Juz', count: milestone_data.completed5, color: 'bg-blue-500'},
    {label: '10 Juz', count: milestone_data.completed10, color: 'bg-green-500'},
    {label: '15 Juz', count: milestone_data.completed15, color: 'bg-yellow-500'},
    {label: '20 Juz', count: milestone_data.completed20, color: 'bg-orange-500'},
    {label: '25 Juz', count: milestone_data.completed25, color: 'bg-purple-500'},
    {label: '30 Juz (Hafiz)', count: milestone_data.completed30, color: 'bg-primary'},
])

const students_by_juz = $derived({
    '0-5': students.filter(student => student.totalJuzMemorized <= 5).length,
    '6-10': students.filter(student => student.totalJuzMemorized >= 6 && student.totalJuzMemorized <= 10).length,
    '11-15': students.filter(student => student.totalJuzMemorized >= 11 && student.totalJuzMemorized <= 15).length,
    '16-20': students.filter(student => student.totalJuzMemorized >= 16 && student.totalJuzMemorized <= 20).length,
    '21-25': students.filter(student => student.totalJuzMemorized >= 21 && student.totalJuzMemorized <= 25).length,
    '26-30': students.filter(student => student.totalJuzMemorized >= 26).length,
})

const milestone_steps = [5, 10, 15, 20, 25, 30]
const percent_steps = [25, 50, 75, 100]
const surah_steps = [10, 30, 60, 114]

const top_columns = [
    {key: 'student', header: 'Student'},
    {key: 'new_ayahs', header: 'New Ayahs', class_name: 'text-center'},
    {key: 'new_surahs', header: 'New Surahs', class_name: 'text-center'},
    {key: 'lessons', header: 'Lessons', class_name: 'text-center'},
]

const teacher_columns = [
    {key: 'teacher', header: 'Teacher'},
    {key: 'students', header: 'Students', class_name: 'text-center'},
    {key: 'lessons', header: 'Lessons', class_name: 'text-center'},
    {key: 'ayahs', header: 'Ayahs Reviewed', class_name: 'text-center'},
    {key: 'surahs', header: 'Surahs Reviewed', class_name: 'text-center'},
    {key: 'assessments', header: 'Upcoming Assessments', class_name: 'text-center'},
]

const attendance_columns = [
    {key: 'student', header: 'Student'},
    {key: 'present', header: 'Present', class_name: 'text-center'},
    {key: 'absent', header: 'Absent', class_name: 'text-center'},
    {key: 'rate', header: 'Rate', class_name: 'text-center'},
]

const homework_columns = [
    {key: 'student', header: 'Student'},
    {key: 'passed', header: 'Passed', class_name: 'text-center'},
    {key: 'failed', header: 'Failed', class_name: 'text-center'},
    {key: 'rate', header: 'Pass Rate', class_name: 'text-center'},
]

const assessment_columns = [
    {key: 'student', header: 'Student'},
    {key: 'average', header: 'Average', class_name: 'text-center'},
    {key: 'last', header: 'Last Score', class_name: 'text-center'},
    {key: 'date', header: 'Last Date', class_name: 'text-center'},
    {key: 'type', header: 'Type', class_name: 'text-center'},
]

const goal_columns = [
    {key: 'student', header: 'Student'},
    {key: 'goal', header: 'Goal Juz', class_name: 'text-center'},
    {key: 'progress', header: 'Progress', class_name: 'text-center'},
    {key: 'status', header: 'Status', class_name: 'text-center'},
]

function top_row_key(item) {
    return item.student.id
}

function teacher_row_key(item) {
    return item.teacher.id
}

function attendance_row_key(item) {
    return item.student.id
}

function homework_row_key(item) {
    return item.student.id
}

function assessment_row_key(item) {
    return item.student.id
}

function goal_row_key(item) {
    return item.student.id
}

function csv_escape(value) {
    if (value === null || value === undefined) return ''
    const text = String(value)
    if (text.includes('"') || text.includes(',') || text.includes('\n')) {
        return `"${text.replaceAll('"', '""')}"`
    }
    return text
}

function push_section(lines, title, headers, rows) {
    lines.push(title)
    lines.push(headers.map(csv_escape).join(','))
    rows.forEach(row => {
        lines.push(row.map(csv_escape).join(','))
    })
    lines.push('')
}

function export_reports() {
    const lines = []
    push_section(lines, 'Program Overview', ['Metric', 'Value'], [
        ['Total students', stats?.totalStudents ?? 0],
        ['Active students', stats?.activeStudents ?? 0],
        ['Total juz memorized', stats?.totalJuzMemorized ?? 0],
        ['Total ayahs memorized', stats?.totalAyahsMemorized ?? 0],
        ['Average rate (ayahs/week)', stats?.averageMemorizationRate ?? 0],
        ['Retention rate', `${retention_rate}%`],
        ['Avg completion time', average_completion_label],
    ])

    push_section(lines, 'Milestone Counts', ['Milestone', 'Students'], [
        ['5 Juz', milestone_data.completed5],
        ['10 Juz', milestone_data.completed10],
        ['15 Juz', milestone_data.completed15],
        ['20 Juz', milestone_data.completed20],
        ['25 Juz', milestone_data.completed25],
        ['30 Juz', milestone_data.completed30],
    ])

    push_section(lines, 'Top Memorizers', ['Student', 'New Ayahs', 'New Surahs', 'Lessons'], top_memorizers.map(item => [
        item.student?.name ?? 'Unknown',
        item.newAyahs,
        item.newSurahs,
        item.lessonCount,
    ]))

    push_section(lines, 'Teacher Workload', ['Teacher', 'Students', 'Lessons', 'Ayahs', 'Surahs', 'Upcoming Assessments'], teacher_workload.map(item => [
        item.teacher?.name ?? 'Unknown',
        item.studentCount,
        item.lessonCount,
        item.totalAyahs,
        item.totalSurahs,
        item.upcomingAssessments,
    ]))

    push_section(lines, 'Attendance Report', ['Student', 'Present', 'Absent', 'Rate'], attendance_report.map(item => [
        item.student?.name ?? 'Unknown',
        item.presentCount,
        item.absentCount,
        `${item.attendanceRate}%`,
    ]))

    push_section(lines, 'Homework Report', ['Student', 'Passed', 'Failed', 'Pass Rate'], homework_report.map(item => [
        item.student?.name ?? 'Unknown',
        item.passedCount,
        item.failedCount,
        `${item.passRate}%`,
    ]))

    push_section(lines, 'Assessment Results', ['Student', 'Average', 'Last Score', 'Last Date', 'Type'], assessments_report.items.map(item => [
        item.student?.name ?? 'Unknown',
        item.averageScore,
        item.lastScore,
        item.lastDate,
        item.lastType,
    ]))

    push_section(lines, 'Goals vs Actual', ['Student', 'Goal Juz', 'Progress', 'Status'], goals_report.map(item => [
        item.student?.name ?? 'Unknown',
        item.goalJuz,
        `${item.progressPercent}%`,
        item.status,
    ]))

    push_section(lines, 'Struggling Students', ['Student', 'Avg Ayahs/Week', 'Reasons'], struggling_students.map(item => [
        item.student?.name ?? 'Unknown',
        item.averageAyahsPerWeek,
        (item.reasons ?? []).join(' | '),
    ]))

    const blob = new Blob([lines.join('\n')], {type: 'text/csv;charset=utf-8;'})
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `quran-reports-${new Date().toISOString().slice(0, 10)}.csv`
    link.click()
    URL.revokeObjectURL(link.href)
}

async function load_data() {
    is_loading = true
    const [
        stats_response,
        students_response,
        milestone_response,
        top_response,
        revision_response,
        teacher_response,
        attendance_response,
        homework_response,
        assessments_response,
        goals_response,
        struggling_response,
    ] = await Promise.all([
        api_get('/api/dashboard/stats'),
        api_get('/api/students'),
        api_get('/api/reports/milestones'),
        api_get('/api/reports/top-memorizers'),
        api_get('/api/reports/revision-status'),
        api_get('/api/reports/teacher-workload'),
        api_get('/api/reports/attendance'),
        api_get('/api/reports/homework'),
        api_get('/api/reports/assessments'),
        api_get('/api/reports/goals'),
        api_get('/api/reports/struggling'),
    ])

    stats = stats_response
    students = students_response ?? []
    milestone_report = milestone_response ?? {juzMilestones: {}, percentMilestones: {}, surahMilestones: {}}
    top_memorizers = top_response ?? []
    revision_report = revision_response ?? {overdue: [], due: [], recentlyCompleted: [], murajaOnly: []}
    teacher_workload = teacher_response ?? []
    attendance_report = attendance_response ?? []
    homework_report = homework_response ?? []
    assessments_report = assessments_response ?? {averageScore: 0, items: []}
    goals_report = goals_response ?? []
    struggling_students = struggling_response ?? []
    is_loading = false
}

;(async () => {
    await load_data()
})()
</script>
