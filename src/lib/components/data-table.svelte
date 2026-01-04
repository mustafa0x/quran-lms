<script>
import {Skeleton} from '$ui/skeleton/index.js'
import * as Table from '$ui/table/index.js'

let {
    columns = [],
    data = [],
    is_loading = false,
    empty_message = 'No data available',
    row_click,
    get_row_key,
    test_id_prefix = 'table',
    cell,
} = $props()

const skeleton_rows = Array.from({length: 5})
</script>

{#if is_loading}
    <div class="rounded-md border">
        <Table.Root>
            <Table.Header>
                <Table.Row>
                    {#each columns as column (column.key)}
                        <Table.Head class={column.class_name}>{column.header}</Table.Head>
                    {/each}
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {#each skeleton_rows as _, index (index)}
                    <Table.Row>
                        {#each columns as column (column.key)}
                            <Table.Cell>
                                <Skeleton class="h-5 w-full" />
                            </Table.Cell>
                        {/each}
                    </Table.Row>
                {/each}
            </Table.Body>
        </Table.Root>
    </div>
{:else if data.length === 0}
    <div class="flex h-48 items-center justify-center rounded-md border border-dashed">
        <p class="text-sm text-muted-foreground">{empty_message}</p>
    </div>
{:else}
    <div class="rounded-md border">
        <Table.Root>
            <Table.Header>
                <Table.Row>
                    {#each columns as column (column.key)}
                        <Table.Head class={column.class_name}>{column.header}</Table.Head>
                    {/each}
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {#each data as item, index (get_row_key ? get_row_key(item) : index)}
                    <Table.Row
                        onclick={() => row_click?.(item)}
                        class={row_click ? 'cursor-pointer hover-elevate' : undefined}
                        data-testid={`${test_id_prefix}-row-${get_row_key ? get_row_key(item) : index}`}
                    >
                        {#each columns as column (column.key)}
                            <Table.Cell class={column.class_name}>
                                {#if cell}
                                    {@render cell(item, column)}
                                {:else}
                                    {item?.[column.key] ?? '-'}
                                {/if}
                            </Table.Cell>
                        {/each}
                    </Table.Row>
                {/each}
            </Table.Body>
        </Table.Root>
    </div>
{/if}
