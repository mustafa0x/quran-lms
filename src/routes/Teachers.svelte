{#snippet actions()}
    <Button onclick={open_add} data-testid="button-add-teacher">
        <PlusIcon class="mr-2 h-4 w-4" />
        Add Teacher
    </Button>
{/snippet}

<PageHeader
    title="Teachers"
    description="Manage your Quran memorization teachers"
    {actions}
/>

<div class="space-y-6">
    <div class="relative max-w-sm">
        <SearchIcon class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
            placeholder="Search teachers..."
            class="pl-9"
            bind:value={search_query}
            data-testid="input-search-teachers"
        />
    </div>

    {#snippet cell(teacher, column)}
        {#if column.key === 'name'}
            <div class="flex items-center gap-3">
                <div class="flex h-9 w-9 items-center justify-center rounded-full bg-primary/10 text-sm font-medium text-primary">
                    {teacher.name.charAt(0).toUpperCase()}
                </div>
                <span class="font-medium">{teacher.name}</span>
            </div>
        {:else if column.key === 'email'}
            <span class="text-muted-foreground">{teacher.email}</span>
        {:else if column.key === 'students'}
            <div class="flex items-center gap-2">
                <UsersIcon class="h-4 w-4 text-muted-foreground" />
                <span>{teacher.studentCount ?? 0}</span>
            </div>
        {:else if column.key === 'actions'}
            <div class="flex items-center justify-end gap-1">
                <Button
                    variant="ghost"
                    size="icon"
                    onclick={() => open_view(teacher)}
                    data-testid={`button-view-teacher-${teacher.id}`}
                >
                    <UsersIcon class="h-4 w-4" />
                </Button>
                <Button
                    variant="ghost"
                    size="icon"
                    onclick={() => open_edit(teacher)}
                    data-testid={`button-edit-teacher-${teacher.id}`}
                >
                    <EditIcon class="h-4 w-4" />
                </Button>
                <Button
                    variant="ghost"
                    size="icon"
                    onclick={() => open_delete(teacher)}
                    data-testid={`button-delete-teacher-${teacher.id}`}
                >
                    <TrashIcon class="h-4 w-4 text-destructive" />
                </Button>
            </div>
        {/if}
    {/snippet}

    <DataTable
        {columns}
        data={filtered_teachers}
        {cell}
        get_row_key={row_key}
        test_id_prefix="teachers"
        is_loading={is_loading}
        empty_message="No teachers found. Add your first teacher to get started."
    />
</div>

<Dialog.Root bind:open={is_form_open}>
    <Dialog.Content>
        <Dialog.Header>
            <Dialog.Title>{editing_teacher ? 'Edit Teacher' : 'Add New Teacher'}</Dialog.Title>
        </Dialog.Header>
        <form class="space-y-4" onsubmit={submit_form}>
            <div class="space-y-2">
                <Label>Name</Label>
                <Input
                    placeholder="Enter teacher name"
                    bind:value={form_state.name}
                    data-testid="input-teacher-name"
                />
            </div>
            <div class="space-y-2">
                <Label>Email</Label>
                <Input
                    type="email"
                    placeholder="Enter email address"
                    bind:value={form_state.email}
                    data-testid="input-teacher-email"
                />
            </div>
            <Dialog.Footer>
                <Button type="submit" disabled={is_saving} data-testid="button-submit-teacher">
                    {is_saving ? 'Saving...' : 'Save Teacher'}
                </Button>
            </Dialog.Footer>
        </form>
    </Dialog.Content>
</Dialog.Root>

<Dialog.Root bind:open={is_view_open}>
    <Dialog.Content class="max-w-lg">
        <Dialog.Header>
            <Dialog.Title>Teacher's Students</Dialog.Title>
        </Dialog.Header>
        {#if viewing_teacher}
            <div class="space-y-4">
                <div class="flex items-center gap-3">
                    <div class="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-lg font-bold text-primary">
                        {viewing_teacher.name.charAt(0).toUpperCase()}
                    </div>
                    <div>
                        <p class="font-semibold">{viewing_teacher.name}</p>
                        <p class="text-sm text-muted-foreground">{viewing_teacher.email}</p>
                    </div>
                </div>

                <Card.Root>
                    <Card.Header class="pb-3">
                        <Card.Title class="text-base">Assigned Students</Card.Title>
                    </Card.Header>
                    <Card.Content>
                        {#if teacher_students.length > 0}
                            <div class="space-y-3">
                                {#each teacher_students as student (student.id)}
                                    <div class="flex items-center justify-between rounded-md border p-3">
                                        <div class="flex items-center gap-3">
                                            <div class="flex h-8 w-8 items-center justify-center rounded-full bg-muted text-sm font-medium">
                                                {student.name.charAt(0).toUpperCase()}
                                            </div>
                                            <span class="font-medium">{student.name}</span>
                                        </div>
                                        <span class="text-sm text-muted-foreground">Juz {student.currentJuz}</span>
                                    </div>
                                {/each}
                            </div>
                        {:else}
                            <p class="text-center text-sm text-muted-foreground py-4">No students assigned yet</p>
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
            <AlertDialog.Title>Delete Teacher</AlertDialog.Title>
            <AlertDialog.Description>
                Are you sure you want to delete {deleting_teacher?.name}? This action cannot be undone.
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
import PlusIcon from '@lucide/svelte/icons/plus'
import SearchIcon from '@lucide/svelte/icons/search'
import TrashIcon from '@lucide/svelte/icons/trash-2'
import UsersIcon from '@lucide/svelte/icons/users'

import {toast} from 'svelte-sonner'

import {api_get, api_request} from '$lib/api.js'
import * as AlertDialog from '$ui/alert-dialog/index.js'
import {Button} from '$ui/button/index.js'
import * as Card from '$ui/card/index.js'
import * as Dialog from '$ui/dialog/index.js'
import {Input} from '$ui/input/index.js'
import {Label} from '$ui/label/index.js'
import DataTable from '$lib/components/data-table.svelte'
import PageHeader from '$lib/components/page-header.svelte'

let teachers = $state([])
let teacher_students = $state([])
let is_loading = $state(true)
let is_saving = $state(false)

let search_query = $state('')

let is_form_open = $state(false)
let is_view_open = $state(false)
let is_delete_open = $state(false)

let editing_teacher = $state(null)
let viewing_teacher = $state(null)
let deleting_teacher = $state(null)

let form_state = $state({
    name: '',
    email: '',
})

const filtered_teachers = $derived(
    teachers.filter(teacher =>
        teacher.name.toLowerCase().includes(search_query.toLowerCase())
        || teacher.email.toLowerCase().includes(search_query.toLowerCase()),
    ),
)

const columns = [
    {key: 'name', header: 'Name'},
    {key: 'email', header: 'Email'},
    {key: 'students', header: 'Students'},
    {key: 'actions', header: '', class_name: 'text-right'},
]

function row_key(teacher) {
    return teacher.id
}

function reset_form_state(teacher = null) {
    if (teacher) {
        form_state = {
            name: teacher.name,
            email: teacher.email,
        }
        return
    }

    form_state = {
        name: '',
        email: '',
    }
}

function open_add() {
    editing_teacher = null
    reset_form_state()
    is_form_open = true
}

function open_edit(teacher) {
    editing_teacher = teacher
    reset_form_state(teacher)
    is_form_open = true
}

async function open_view(teacher) {
    viewing_teacher = teacher
    is_view_open = true
    teacher_students = (await api_get('/api/students', {teacherId: teacher.id})) ?? []
}

function open_delete(teacher) {
    deleting_teacher = teacher
    is_delete_open = true
}

async function load_teachers() {
    is_loading = true
    teachers = (await api_get('/api/teachers')) ?? []
    is_loading = false
}

async function submit_form(event) {
    event.preventDefault()
    is_saving = true

    const payload = {
        name: form_state.name.trim(),
        email: form_state.email.trim(),
    }

    const response = editing_teacher
        ? await api_request('PATCH', `/api/teachers/${editing_teacher.id}`, payload)
        : await api_request('POST', '/api/teachers', payload)

    if (response === false) {
        toast.error(editing_teacher ? 'Failed to update teacher' : 'Failed to add teacher')
        is_saving = false
        return
    }

    toast.success(editing_teacher ? 'Teacher updated successfully' : 'Teacher added successfully')
    is_form_open = false
    editing_teacher = null
    is_saving = false
    await load_teachers()
}

async function confirm_delete() {
    if (!deleting_teacher) return
    const response = await api_request('DELETE', `/api/teachers/${deleting_teacher.id}`)
    if (response === false) {
        toast.error('Failed to delete teacher')
        return
    }
    toast.success('Teacher deleted successfully')
    is_delete_open = false
    deleting_teacher = null
    await load_teachers()
}

;(async () => {
    await load_teachers()
})()
</script>
