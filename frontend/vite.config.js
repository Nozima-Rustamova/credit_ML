import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite config with proxy so API calls to /api are forwarded to Django dev server
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
