import js from '@eslint/js'
import {defineConfig} from 'eslint/config'
import eslintPluginImportX from 'eslint-plugin-import-x'
import simpleImportSort from 'eslint-plugin-simple-import-sort'
import svelte from 'eslint-plugin-svelte'
import globals from 'globals'

/** @param {string} s */
const prep_globals = s => Object.fromEntries(s.split(' ').map(g => [g, 'readonly']))
const globals_all = {
    ...prep_globals('Sentry'),
}

export default defineConfig(
    js.configs.recommended,
    ...svelte.configs.recommended,
    {
        ignores: [
            ...'node_modules,dist,dist-native,android,ios,public,misc,.venv,src/lib/components/ui/'
                .split(',')
                .map(x => x + '/**/*'),
            '**/*.svelte.ts',
        ],
    },
    {
        rules: {
            'no-empty': ['error', {allowEmptyCatch: true}],
            'no-misleading-character-class': 'off',
            'svelte/prefer-svelte-reactivity': 'off',
            'no-unused-vars': ['error', {argsIgnorePattern: '^_', varsIgnorePattern: '^_'}],
        },
    },
    {
        files: ['src/**/*.js'],
        languageOptions: {
            globals: {...globals.es2021, ...globals.browser, ...globals_all},
        },
    },
    {
        files: ['deploy.js', 'eslint.config.js', 'prettier.config.js', 'vite.config.js'],
        languageOptions: {
            globals: {...globals.es2021, ...globals.node},
        },
    },
    {
        files: ['**/*.svelte', '**/*.svelte.js'],
        languageOptions: {
            globals: {...globals.es2021, ...globals.browser, ...globals_all},
        },
    },
    {
        files: ['**/*.svelte'],
        rules: {
            'no-inner-declarations': 'off',
            'svelte/no-at-html-tags': 'off',
            'svelte/require-each-key': 'off',
            'svelte/valid-compile': ['error', {ignoreWarnings: true}],
        },
    },
    {
        plugins: {
            'simple-import-sort': simpleImportSort,
            'import-x': eslintPluginImportX,
        },
        rules: {
            'simple-import-sort/imports': 'error',
            'simple-import-sort/exports': 'error',
            'import-x/first': 'error',
            'import-x/newline-after-import': 'error',
            'import-x/no-duplicates': 'error',
            'import-x/extensions': [
                'error',
                'always',
                {
                    ignorePackages: true,
                },
            ],
        },
    },
)
