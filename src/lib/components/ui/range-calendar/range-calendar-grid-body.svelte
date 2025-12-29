<RangeCalendarPrimitive.GridBody bind:ref {...restProps} />

<script lang="ts">
import {RangeCalendar as RangeCalendarPrimitive} from 'bits-ui'

let {ref = $bindable(null), ...restProps}: RangeCalendarPrimitive.GridBodyProps = $props()
</script>
