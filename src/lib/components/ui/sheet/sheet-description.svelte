<SheetPrimitive.Description
    bind:ref
    data-slot="sheet-description"
    class={cn('text-sm text-muted-foreground', className)}
    {...restProps}
/>

<script lang="ts">
import {Dialog as SheetPrimitive} from 'bits-ui'
import {cn} from '$lib/utils.js'

let {
    ref = $bindable(null),
    class: className,
    ...restProps
}: SheetPrimitive.DescriptionProps = $props()
</script>
