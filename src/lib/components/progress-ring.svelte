<script>
let {
    value,
    max,
    size = 120,
    stroke_width = 10,
    class: class_name = '',
    label,
} = $props()

const radius = $derived((size - stroke_width) / 2)
const circumference = $derived(radius * 2 * Math.PI)
const percentage = $derived(max ? Math.min((value / max) * 100, 100) : 0)
const offset = $derived(circumference - (percentage / 100) * circumference)
</script>

<div class="relative inline-flex items-center justify-center {class_name}">
    <svg width={size} height={size} class="-rotate-90">
        <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke-width={stroke_width}
            class="fill-none stroke-muted"
        ></circle>
        <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke-width={stroke_width}
            stroke-dasharray={circumference}
            stroke-dashoffset={offset}
            stroke-linecap="round"
            class="fill-none stroke-primary transition-all duration-500"
        ></circle>
    </svg>
    <div class="absolute flex flex-col items-center justify-center">
        <span class="text-2xl font-bold">{value}</span>
        {#if label}
            <span class="text-xs text-muted-foreground">{label}</span>
        {/if}
    </div>
</div>
