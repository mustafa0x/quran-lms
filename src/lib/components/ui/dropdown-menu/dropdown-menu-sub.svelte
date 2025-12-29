<DropdownMenuPrimitive.Sub bind:open {...restProps} />

<script lang="ts">
import {DropdownMenu as DropdownMenuPrimitive} from 'bits-ui'

let {open = $bindable(false), ...restProps}: DropdownMenuPrimitive.SubProps = $props()
</script>
