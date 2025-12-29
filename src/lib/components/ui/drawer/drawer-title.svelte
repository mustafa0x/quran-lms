<DrawerPrimitive.Title
    bind:ref
    data-slot="drawer-title"
    class={cn('font-semibold text-foreground', className)}
    {...restProps}
/>

<script lang="ts">
import {Drawer as DrawerPrimitive} from 'vaul-svelte'
import {cn} from '$lib/utils.js'

let {ref = $bindable(null), class: className, ...restProps}: DrawerPrimitive.TitleProps = $props()
</script>
