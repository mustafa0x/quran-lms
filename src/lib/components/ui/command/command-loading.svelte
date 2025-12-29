<CommandPrimitive.Loading bind:ref {...restProps} />

<script lang="ts">
import {Command as CommandPrimitive} from 'bits-ui'

let {ref = $bindable(null), ...restProps}: CommandPrimitive.LoadingProps = $props()
</script>
