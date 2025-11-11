import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    // Output directory for production build
    outDir: 'dist',
    // Generate sourcemaps for production debugging
    sourcemap: false,
    // Optimize build
    minify: 'terser',
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
