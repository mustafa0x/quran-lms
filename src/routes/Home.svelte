<Sidebar.Provider>
    <AppSidebar />

    <div class="min-h-dvh bg-background text-foreground antialiased" transition:fade>
        <Nav />

        <main class="flex flex-col">
            <div class="mb-4 flex items-center">
                <Sidebar.Trigger />
            </div>

            <Hero />
            <Features />
            <DemoShowcase />
        </main>

        <Footer />
    </div>
</Sidebar.Provider>

<script>
import {fade} from 'svelte/transition'

import DemoShowcase from '~/components/demo-showcase.svelte'
import Features from '~/components/feature/features.svelte'
import Footer from '~/components/footer.svelte'
import Hero from '~/components/hero/hero.svelte'
import Nav from '~/components/nav/nav.svelte'
import AppSidebar from '$lib/components/app-sidebar.svelte'
import * as Sidebar from '$ui/sidebar/index.js'
</script>
