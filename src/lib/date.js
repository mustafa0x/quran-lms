export function format_date_input(value) {
    const date = value instanceof Date ? value : new Date(value)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
}

export function format_month_year(date) {
    return date.toLocaleDateString('en-US', {month: 'long', year: 'numeric'})
}

export function format_readable_date(date) {
    return date.toLocaleDateString('en-US', {month: 'long', day: 'numeric', year: 'numeric'})
}

export function format_month_key(date) {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    return `${year}-${month}`
}

export function start_of_month(date) {
    return new Date(date.getFullYear(), date.getMonth(), 1)
}

export function end_of_month(date) {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0)
}

export function each_day_of_interval(start, end) {
    const days = []
    const current = new Date(start)
    while (current <= end) {
        days.push(new Date(current))
        current.setDate(current.getDate() + 1)
    }
    return days
}

export function is_same_day(a, b) {
    return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate()
}

export function add_months(date, amount) {
    const next = new Date(date)
    next.setMonth(next.getMonth() + amount)
    return next
}
