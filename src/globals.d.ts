/// <reference types="vite/types/importMeta.d.ts" />
declare global {
    interface Window {
        __BUILD_DATE__: string
        __BUILD_HASH__: string
        __APP_VERSION__: string

        __DEBUG__: boolean
        BASE_TITLE: string
        _VH_OFFSET: number
        _useragent: {ios: string; safari: string; no_keyboard: string}

        navgo: import('navgo').Router
        Sentry: {
            captureMessage: (message: string) => void
            captureException: (exception: unknown) => void
        }
    }
}
export {}
