import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Exposes the server on the local network
    port: 5173, // Ensures this matches the port you're exposing in Docker
    strictPort: true, // Ensures Vite will not switch ports if 5173 is taken
    watch: {
      usePolling: true, // Necessary for Docker, as file changes might not be detected otherwise
    },
  },
});
