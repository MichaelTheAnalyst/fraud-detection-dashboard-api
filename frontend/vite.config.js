import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },
  build: {
    // Ensure CSS is properly extracted and minified
    cssCodeSplit: false,
    // Optimize for production
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: false, // Keep console logs for debugging
      },
    },
    // Increase chunk size warning limit
    chunkSizeWarningLimit: 1000,
    // Ensure all assets are included
    assetsInclude: ['**/*.css'],
    rollupOptions: {
      output: {
        // Ensure CSS is in a single file for better loading
        assetFileNames: 'assets/[name].[ext]',
      },
    },
  },
  // Ensure CSS is processed correctly
  css: {
    postcss: './postcss.config.js',
  },
})

