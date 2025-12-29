<PageHeader title="Dashboard" description="Overview of your Quran memorization program" />

<div class="space-y-6">
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {#if stats_loading}
            {#each Array.from({length: 4}) as _, index (index)}
                <Card.Root>
                    <Card.Content class="p-6">
                        <Skeleton class="h-20 w-full" />
                    </Card.Content>
                </Card.Root>
            {/each}
        {:else}
            <StatCard
                title="Total Students"
                value={stats?.totalStudents ?? 0}
                subtitle={`${stats?.activeStudents ?? 0} active`}
                icon={UsersIcon}
                test_id="stat-total-students"
            />
            <StatCard
                title="Total Teachers"
                value={stats?.totalTeachers ?? 0}
                icon={GraduationCapIcon}
                test_id="stat-total-teachers"
            />
            <StatCard
                title="Juz Memorized"
                value={stats?.totalJuzMemorized ?? 0}
                subtitle="Across all students"
                icon={BookOpenIcon}
                test_id="stat-juz-memorized"
            />
            <StatCard
                title="Attendance Rate"
                value={`${stats?.attendanceRate ?? 0}%`}
                subtitle="This month"
                icon={CalendarIcon}
                test_id="stat-attendance"
            />
        {/if}
    </div>

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {#if stats_loading}
            {#each Array.from({length: 3}) as _, index (index)}
                <Card.Root>
                    <Card.Content class="p-6">
                        <Skeleton class="h-16 w-full" />
                    </Card.Content>
                </Card.Root>
            {/each}
        {:else}
            <Card.Root>
                <Card.Content class="flex items-center gap-4 p-6">
                    <div class="flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
                        <CheckCircleIcon class="h-6 w-6 text-green-600 dark:text-green-400" />
                    </div>
                    <div>
                        <p class="text-sm text-muted-foreground">Lessons Today</p>
                        <p class="text-2xl font-bold" data-testid="stat-lessons-today">{stats?.lessonsToday ?? 0}</p>
                    </div>
                </Card.Content>
            </Card.Root>
            <Card.Root>
                <Card.Content class="flex items-center gap-4 p-6">
                    <div class="flex h-12 w-12 items-center justify-center rounded-full bg-amber-100 dark:bg-amber-900/30">
                        <AlertTriangleIcon class="h-6 w-6 text-amber-600 dark:text-amber-400" />
                    </div>
                    <div>
                        <p class="text-sm text-muted-foreground">Overdue Muraja'ah</p>
                        <p class="text-2xl font-bold" data-testid="stat-overdue-muraja">{stats?.studentsOverdueMuraja ?? 0}</p>
                    </div>
                </Card.Content>
            </Card.Root>
            <Card.Root>
                <Card.Content class="flex items-center gap-4 p-6">
                    <div class="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-900/30">
                        <TrendingUpIcon class="h-6 w-6 text-blue-600 dark:text-blue-400" />
                    </div>
                    <div>
                        <p class="text-sm text-muted-foreground">Avg. Rate</p>
                        <p class="text-2xl font-bold" data-testid="stat-avg-rate">{stats?.averageMemorizationRate ?? 0} ayahs/week</p>
                    </div>
                </Card.Content>
            </Card.Root>
        {/if}
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
        <Card.Root>
            <Card.Header class="flex flex-row items-center justify-between gap-4 space-y-0 pb-4">
                <Card.Title class="text-lg font-semibold">Recent Students</Card.Title>
            </Card.Header>
            <Card.Content>
                {#if students_loading}
                    <div class="space-y-4">
                        {#each Array.from({length: 5}) as _, index (index)}
                            <div class="flex items-center gap-4">
                                <Skeleton class="h-10 w-10 rounded-full" />
                                <div class="flex-1 space-y-2">
                                    <Skeleton class="h-4 w-3/4" />
                                    <Skeleton class="h-3 w-1/2" />
                                </div>
                            </div>
                        {/each}
                    </div>
                {:else if recent_students.length > 0}
                    <div class="space-y-4">
                        {#each recent_students as student (student.id)}
                            <div class="flex items-center gap-4" data-testid={`recent-student-${student.id}`}>
                                <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 font-semibold text-primary">
                                    {student.name.charAt(0).toUpperCase()}
                                </div>
                                <div class="flex-1 min-w-0">
                                    <p class="font-medium truncate">{student.name}</p>
                                    <p class="text-sm text-muted-foreground">
                                        Juz {student.currentJuz} | {student.totalJuzMemorized} completed
                                    </p>
                                </div>
                                <ProgressRing value={student.totalJuzMemorized} max={30} size={48} stroke_width={4} />
                            </div>
                        {/each}
                    </div>
                {:else}
                    <div class="flex h-32 items-center justify-center">
                        <p class="text-sm text-muted-foreground">No students yet</p>
                    </div>
                {/if}
            </Card.Content>
        </Card.Root>

        <Card.Root>
            <Card.Header class="flex flex-row items-center justify-between gap-4 space-y-0 pb-4">
                <Card.Title class="text-lg font-semibold">Muraja'ah Alerts</Card.Title>
                <ClockIcon class="h-5 w-5 text-muted-foreground" />
            </Card.Header>
            <Card.Content>
                {#if revisions_loading}
                    <div class="space-y-4">
                        {#each Array.from({length: 5}) as _, index (index)}
                            <div class="flex items-center gap-4">
                                <Skeleton class="h-8 w-8 rounded" />
                                <div class="flex-1 space-y-2">
                                    <Skeleton class="h-4 w-3/4" />
                                    <Skeleton class="h-3 w-1/2" />
                                </div>
                            </div>
                        {/each}
                    </div>
                {:else if overdue_revisions.length > 0}
                    <div class="space-y-3">
                        {#each overdue_revisions as revision (revision.id)}
                            <div class="flex items-center justify-between gap-4 rounded-md border p-3" data-testid={`overdue-revision-${revision.id}`}>
                                <div class="min-w-0">
                                    <p class="font-medium truncate">{revision.student?.name ?? 'Unknown Student'}</p>
                                    <p class="text-sm text-muted-foreground">Due: {revision.nextRevisionDueDate ?? 'Not scheduled'}</p>
                                </div>
                                <StatusBadge status={get_muraja_status_type(revision.overdue)}>
                                    {revision.overdue ? 'Overdue' : 'On Track'}
                                </StatusBadge>
                            </div>
                        {/each}
                    </div>
                {:else}
                    <div class="flex h-32 items-center justify-center">
                        <div class="text-center">
                            <CheckCircleIcon class="mx-auto h-8 w-8 text-green-500" />
                            <p class="mt-2 text-sm text-muted-foreground">All revisions are on track</p>
                        </div>
                    </div>
                {/if}
            </Card.Content>
        </Card.Root>
    </div>
</div>

<script>
import AlertTriangleIcon from '@lucide/svelte/icons/alert-triangle'
import BookOpenIcon from '@lucide/svelte/icons/book-open'
import CalendarIcon from '@lucide/svelte/icons/calendar'
import CheckCircleIcon from '@lucide/svelte/icons/check-circle'
import ClockIcon from '@lucide/svelte/icons/clock'
import GraduationCapIcon from '@lucide/svelte/icons/graduation-cap'
import TrendingUpIcon from '@lucide/svelte/icons/trending-up'
import UsersIcon from '@lucide/svelte/icons/users'

import {api_get} from '$lib/api.js'
import * as Card from '$ui/card/index.js'
import {Skeleton} from '$ui/skeleton/index.js'
import PageHeader from '$lib/components/page-header.svelte'
import ProgressRing from '$lib/components/progress-ring.svelte'
import StatCard from '$lib/components/stat-card.svelte'
import StatusBadge, {get_muraja_status_type} from '$lib/components/status-badge.svelte'

let stats = $state(null)
let stats_loading = $state(true)
let recent_students = $state([])
let students_loading = $state(true)
let overdue_revisions = $state([])
let revisions_loading = $state(true)

async function load_stats() {
    stats_loading = true
    stats = await api_get('/api/dashboard/stats')
    stats_loading = false
}

async function load_recent_students() {
    students_loading = true
    recent_students = (await api_get('/api/students', {limit: 5})) ?? []
    students_loading = false
}

async function load_overdue_revisions() {
    revisions_loading = true
    overdue_revisions = (await api_get('/api/muraja/overdue')) ?? []
    revisions_loading = false
}

;(async () => {
    await load_stats()
    await load_recent_students()
    await load_overdue_revisions()
})()
</script>
