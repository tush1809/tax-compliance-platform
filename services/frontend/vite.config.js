import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://api-gateway:8080', // name of the container in docker-compose
        changeOrigin: true,
        secure: false,
      },
    },
  },
});

