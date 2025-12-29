<DialogPrimitive.Root bind:open {...restProps} />

<script lang="ts">
import {Dialog as DialogPrimitive} from 'bits-ui'

let {open = $bindable(false), ...restProps}: DialogPrimitive.RootProps = $props()
</script>
