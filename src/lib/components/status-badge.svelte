<script module>
export const status_styles = {
    success: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    warning: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400',
    error: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    info: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    neutral: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300',
}

export function get_student_status_type(status) {
    return status === 'active' ? 'success' : 'neutral'
}

export function get_rating_status_type(rating) {
    if (rating === 'Pass') return 'success'
    if (rating === 'Re-do') return 'warning'
    if (rating === 'Absent') return 'error'
    return 'neutral'
}

export function get_attendance_status_type(present) {
    return present ? 'success' : 'error'
}

export function get_muraja_status_type(overdue) {
    return overdue ? 'error' : 'success'
}
</script>

<script>
import {Badge} from '$ui/badge/index.js'

let {status = 'neutral', children, test_id} = $props()
</script>

<Badge variant="secondary" class="{status_styles[status] ?? status_styles.neutral} border-0" data-testid={test_id}>
    {@render children?.()}
</Badge>
