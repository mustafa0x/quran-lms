<DrawerPrimitive.Trigger bind:ref data-slot="drawer-trigger" {...restProps} />

<script lang="ts">
import {Drawer as DrawerPrimitive} from 'vaul-svelte'

let {ref = $bindable(null), ...restProps}: DrawerPrimitive.TriggerProps = $props()
</script>
