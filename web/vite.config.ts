import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// The backend has no CORS, so the dev server forwards API calls to it.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/telecom-tmf-bss': { target: 'http://127.0.0.1:8060', changeOrigin: true },
    },
  },
})
