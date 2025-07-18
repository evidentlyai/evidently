import { defineConfig } from 'vite'
import tsconfigPaths from 'vite-tsconfig-paths'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://127.0.0.1:8000'
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
