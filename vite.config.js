import path from 'node:path'

import {svelte} from '@sveltejs/vite-plugin-svelte'
import tailwindcss from '@tailwindcss/vite'
import {execFileSync as exec} from 'child_process'
import {defineConfig} from 'vite'
import domain from 'vite-plugin-domain'

import pkg from './package.json' with {type: 'json'}
import tsconfig from './tsconfig.json' with {type: 'json'}

const is_build = process.argv.includes('build')

const vars = {
    'window.__BUILD_DATE__': `'${new Date().toISOString()}'`,
    'window.__BUILD_HASH__': `'${exec('git rev-parse --short HEAD || true', {shell: true}).toString().trim()}'`,
    'window.__APP_VERSION__': `'${pkg.version}'`,
    'window.__DEBUG__': !is_build,
}

export default defineConfig({
    resolve: {
        alias: Object.fromEntries(
            Object.entries(tsconfig.compilerOptions.paths).map(([k, v]) => [
                // '~/*': ['src/*'] => '~': path.resolve('src')
                k.replace('/*', ''),
                path.resolve(v[0].replace('/*', '')),
            ]),
        ),
    },
    publicDir: is_build ? false : 'public',
    css: {
        transformer: 'lightningcss',
    },
    build: {
        reportCompressedSize: false,
        minify: false,
        sourcemap: true,
        cssMinify: 'lightningcss',
        lib: {
            entry: 'src/main.js',
            formats: ['es'],
            fileName: format => `bundle.${format}.js`,
        },
        rollupOptions: {
            input: './index.html',
            output: {
                inlineDynamicImports: true,
                intro: Object.entries(vars)
                    .map(([k, v]) => `${k} = ${v}`)
                    .join('\n'),
                // entryFileNames: '[name].js',
                // chunkFileNames: '[name].js',
                // assetFileNames: '[name][extname]',
            },
        },
    },
    server: {
        watch: {
            ignored: ['android', 'ios', 'dist', 'dist-native'].map(x => `${x}/**`),
        },
        host: !!process.env.VITE_HOST || '0.0.0.0',
        port: +(process.env.VITE_PORT || 5100),
        proxy: {
            '^/api.*': {
                target: `http://127.0.0.1:${process.env.API_PORT || 6000}`,
            },
        },
    },
    define: is_build ? {} : vars,
    plugins: [
        domain({tld: 'localhost'}),
        tailwindcss(),
        svelte({
            onwarn(warning, handler) {
                const IGNORED_WARNINGS = [
                    'a11y_autofocus',
                    'a11y_click_events_have_key_events',
                    'a11y_no_static_element_interactions',
                    'a11y_label_has_associated_control',
                    'a11y_no_noninteractive_element_interactions',
                ]
                if (!IGNORED_WARNINGS.includes(warning.code)) handler(warning)
            },
        }),
    ],
})
