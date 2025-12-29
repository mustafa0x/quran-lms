<RangeCalendarPrimitive.GridHead bind:ref {...restProps} />

<script lang="ts">
import {RangeCalendar as RangeCalendarPrimitive} from 'bits-ui'

let {ref = $bindable(null), ...restProps}: RangeCalendarPrimitive.GridHeadProps = $props()
</script>
