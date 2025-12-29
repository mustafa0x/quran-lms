<Sidebar.Root collapsible="icon">
    <Sidebar.Header class="p-4">
        <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-md bg-primary">
                <BookOpenIcon class="h-5 w-5 text-primary-foreground" />
            </div>
            <div class="flex flex-col">
                <span class="text-base font-semibold">Quran Tracker</span>
                <span class="text-xs text-muted-foreground">Memorization Management</span>
            </div>
        </div>
    </Sidebar.Header>

    <Sidebar.Content>
        <Sidebar.Group>
            <Sidebar.GroupLabel>Main</Sidebar.GroupLabel>
            <Sidebar.GroupContent>
                <Sidebar.Menu>
                    {#each main_items as item (item.title)}
                        {@const Icon = item.icon}
                        <Sidebar.MenuItem>
                            <Sidebar.MenuButton
                                isActive={active_path === item.url}
                                data-testid={`nav-${item.test_id}`}
                                onclick={() => window.navgo.goto(item.url)}
                            >
                                <Icon class="h-4 w-4" />
                                <span>{item.title}</span>
                            </Sidebar.MenuButton>
                        </Sidebar.MenuItem>
                    {/each}
                </Sidebar.Menu>
            </Sidebar.GroupContent>
        </Sidebar.Group>

        <Sidebar.Group>
            <Sidebar.GroupLabel>Tracking</Sidebar.GroupLabel>
            <Sidebar.GroupContent>
                <Sidebar.Menu>
                    {#each tracking_items as item (item.title)}
                        {@const Icon = item.icon}
                        <Sidebar.MenuItem>
                            <Sidebar.MenuButton
                                isActive={active_path === item.url}
                                data-testid={`nav-${item.test_id}`}
                                onclick={() => window.navgo.goto(item.url)}
                            >
                                <Icon class="h-4 w-4" />
                                <span>{item.title}</span>
                            </Sidebar.MenuButton>
                        </Sidebar.MenuItem>
                    {/each}
                </Sidebar.Menu>
            </Sidebar.GroupContent>
        </Sidebar.Group>

        <Sidebar.Group>
            <Sidebar.GroupLabel>Analytics</Sidebar.GroupLabel>
            <Sidebar.GroupContent>
                <Sidebar.Menu>
                    {#each analytics_items as item (item.title)}
                        {@const Icon = item.icon}
                        <Sidebar.MenuItem>
                            <Sidebar.MenuButton
                                isActive={active_path === item.url}
                                data-testid={`nav-${item.test_id}`}
                                onclick={() => window.navgo.goto(item.url)}
                            >
                                <Icon class="h-4 w-4" />
                                <span>{item.title}</span>
                            </Sidebar.MenuButton>
                        </Sidebar.MenuItem>
                    {/each}
                </Sidebar.Menu>
            </Sidebar.GroupContent>
        </Sidebar.Group>
    </Sidebar.Content>

    <Sidebar.Footer class="p-4">
        <Sidebar.Menu>
            <Sidebar.MenuItem>
                <Sidebar.MenuButton
                    isActive={active_path === '/settings'}
                    data-testid="nav-settings"
                    onclick={() => window.navgo.goto('/settings')}
                >
                    <SettingsIcon class="h-4 w-4" />
                    <span>Settings</span>
                </Sidebar.MenuButton>
            </Sidebar.MenuItem>
        </Sidebar.Menu>
    </Sidebar.Footer>
</Sidebar.Root>

<script>
import BookOpenIcon from '@lucide/svelte/icons/book-open'
import BookOpenCheckIcon from '@lucide/svelte/icons/book-open-check'
import CalendarIcon from '@lucide/svelte/icons/calendar'
import ClipboardCheckIcon from '@lucide/svelte/icons/clipboard-check'
import FileTextIcon from '@lucide/svelte/icons/file-text'
import GraduationCapIcon from '@lucide/svelte/icons/graduation-cap'
import LayoutDashboardIcon from '@lucide/svelte/icons/layout-dashboard'
import RefreshCwIcon from '@lucide/svelte/icons/refresh-cw'
import SettingsIcon from '@lucide/svelte/icons/settings'
import StarIcon from '@lucide/svelte/icons/star'
import UsersIcon from '@lucide/svelte/icons/users'

import * as Sidebar from '$ui/sidebar/index.js'

const {route} = window.navgo
const active_path = $derived($route.url.pathname)

const main_items = [
    {
        title: 'Dashboard',
        url: '/',
        icon: LayoutDashboardIcon,
        test_id: 'dashboard',
    },
    {
        title: 'Students',
        url: '/students',
        icon: UsersIcon,
        test_id: 'students',
    },
    {
        title: 'Teachers',
        url: '/teachers',
        icon: GraduationCapIcon,
        test_id: 'teachers',
    },
]

const tracking_items = [
    {
        title: 'Daily Lessons',
        url: '/lessons',
        icon: BookOpenCheckIcon,
        test_id: 'daily-lessons',
    },
    {
        title: "Muraja'ah",
        url: '/muraja',
        icon: RefreshCwIcon,
        test_id: 'muraja',
    },
    {
        title: 'Attendance',
        url: '/attendance',
        icon: CalendarIcon,
        test_id: 'attendance',
    },
    {
        title: 'Homework',
        url: '/homework',
        icon: ClipboardCheckIcon,
        test_id: 'homework',
    },
]

const analytics_items = [
    {
        title: 'Reports',
        url: '/reports',
        icon: FileTextIcon,
        test_id: 'reports',
    },
    {
        title: 'Points',
        url: '/points',
        icon: StarIcon,
        test_id: 'points',
    },
]
</script>
