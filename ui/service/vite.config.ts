import { defineConfig, PluginOption } from 'vite'
import tsconfigPaths from 'vite-tsconfig-paths'
import react from '@vitejs/plugin-react-swc'




// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), tsconfigPaths(), preloadAllScripts()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://127.0.0.1:8000'
      // '/api': 'https://demo.evidentlyai.com'
    }
  },
  build: {
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          const fileName = assetInfo.names?.[0] || 'unknown'
          let [extType] = fileName.split('.').reverse()

          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType)) {
            // don't hash images
            return `static/img/[name][extname]`
          }
          // hash everything else (like css)
          return `static/${extType}/[name]-[hash][extname]`
        },
        chunkFileNames: 'static/js/[name]-[hash].js',
        entryFileNames: 'static/js/[name]-[hash].js'
      }
    }
  }
})


function preloadAllScripts() {
  const [headClosedTag, tabs4, tabs2] = ['</head>', '    ', '  ']

  return {
    name: 'insert modulepreload additional js chunk link tags',
    transformIndexHtml: (html, ctx) => {
      if (!ctx.bundle) {
        return
      }

      const scriptNames = Object.values(ctx.bundle)
        .map(({ type, fileName }) =>
          type === 'asset' || html.includes(fileName)
            ? // return `false` to skip file if
              // file is css/img etc, or if
              // this file already in html
              false
            : fileName
        )
        .filter((e): e is string => typeof e === 'string')

      const modulepreloadLinks = scriptNames
        .map((scriptName) => `${tabs4}<link rel="modulepreload" crossorigin href="/${scriptName}">`)
        .join('\n')

      const additionalLinks = `\n${tabs4}${'<!-- Preload all additional js chunks -->'}\n${modulepreloadLinks}\n${tabs2}`

      return html.replace(headClosedTag, `${additionalLinks}${headClosedTag}`)
    }
  } satisfies PluginOption
}
