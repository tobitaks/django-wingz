import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  // Remove base - we'll handle static files with Django's STATIC_URL
  build: {
    // Output directory for production build
    outDir: 'dist',
    // Use 'assets' directory for built files so they're clearly separated
    assetsDir: 'assets',
    // Generate sourcemaps for production debugging
    sourcemap: false,
    // Use default esbuild minifier (faster than terser)
    minify: 'esbuild',
  },
  server: {
    // Development server configuration
    port: 5173,
    proxy: {
      // Proxy API requests to Django backend during development
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
