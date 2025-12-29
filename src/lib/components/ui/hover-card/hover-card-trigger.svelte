<HoverCardPrimitive.Trigger bind:ref data-slot="hover-card-trigger" {...restProps} />

<script lang="ts">
import {LinkPreview as HoverCardPrimitive} from 'bits-ui'

let {ref = $bindable(null), ...restProps}: HoverCardPrimitive.TriggerProps = $props()
</script>
