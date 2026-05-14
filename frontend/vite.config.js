import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// https://vite.dev/config/
export default defineConfig({
  // Load `.env` from repo root (parent of `frontend/`) so `VITE_*` matches backend env file.
  envDir: path.resolve(__dirname, '..'),
  plugins: [react(), tailwindcss()],
})
