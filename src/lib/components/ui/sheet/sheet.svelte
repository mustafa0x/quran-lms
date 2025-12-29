<SheetPrimitive.Root bind:open {...restProps} />

<script lang="ts">
import {Dialog as SheetPrimitive} from 'bits-ui'

let {open = $bindable(false), ...restProps}: SheetPrimitive.RootProps = $props()
</script>
