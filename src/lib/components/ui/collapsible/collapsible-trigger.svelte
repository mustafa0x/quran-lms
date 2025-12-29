<CollapsiblePrimitive.Trigger bind:ref data-slot="collapsible-trigger" {...restProps} />

<script lang="ts">
import {Collapsible as CollapsiblePrimitive} from 'bits-ui'

let {ref = $bindable(null), ...restProps}: CollapsiblePrimitive.TriggerProps = $props()
</script>
