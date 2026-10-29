import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// base: './' — собранная папка dist открывается с любого статического сервера и из любой подпапки
export default defineConfig({
  base: './',
  plugins: [react()],
});
