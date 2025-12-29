<div class="min-h-screen w-full flex items-center justify-center bg-gray-50">
    <Card.Root class="w-full max-w-md mx-4">
        <Card.Content class="pt-6">
            <div class="flex mb-4 gap-2">
                <AlertCircleIcon class="h-8 w-8 text-red-500" />
                <h1 class="text-2xl font-bold text-gray-900">404 Page Not Found</h1>
            </div>
            <p class="mt-4 text-sm text-gray-600">Did you forget to add the page to the router?</p>
        </Card.Content>
    </Card.Root>
</div>

<script>
import AlertCircleIcon from '@lucide/svelte/icons/alert-circle'

import * as Card from '$ui/card/index.js'
</script>
