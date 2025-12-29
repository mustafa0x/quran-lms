<ContextMenuPrimitive.Root bind:open {...restProps} />

<script lang="ts">
import {ContextMenu as ContextMenuPrimitive} from 'bits-ui'

let {open = $bindable(false), ...restProps}: ContextMenuPrimitive.RootProps = $props()
</script>
