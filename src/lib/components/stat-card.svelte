<script>
import * as Card from '$ui/card/index.js'

let {title, value, subtitle, icon, trend, test_id} = $props()

const Icon = $derived(icon)
</script>

<Card.Root data-testid={test_id}>
    <Card.Content class="p-6">
        <div class="flex items-start justify-between gap-4">
            <div class="flex-1 space-y-1">
                <p class="text-sm text-muted-foreground">{title}</p>
                <p class="text-3xl font-bold tracking-tight" data-testid={test_id ? `${test_id}-value` : undefined}>
                    {value}
                </p>
                {#if subtitle}
                    <p class="text-xs text-muted-foreground">{subtitle}</p>
                {/if}
                {#if trend}
                    <p class="text-xs font-medium {trend.positive ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}">
                        {trend.positive ? '+' : ''}{trend.value}% from last month
                    </p>
                {/if}
            </div>
            {#if Icon}
                <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-md bg-primary/10">
                    <Icon class="h-6 w-6 text-primary" />
                </div>
            {/if}
        </div>
    </Card.Content>
</Card.Root>
