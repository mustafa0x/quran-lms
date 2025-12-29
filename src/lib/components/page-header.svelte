<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
    <div class="space-y-1">
        <h1 class="text-2xl font-bold tracking-tight" data-testid="page-title">{title}</h1>
        {#if description}
            <p class="text-sm text-muted-foreground" data-testid="page-description">{description}</p>
        {/if}
    </div>
    {#if actions}
        <div class="flex flex-wrap items-center gap-2">
            {@render actions()}
        </div>
    {/if}
</div>

<script>
let {title, description = '', actions} = $props()
</script>
