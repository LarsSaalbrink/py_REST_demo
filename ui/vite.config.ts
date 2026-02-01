import { defineConfig } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

// Single minified file for easy serving
export default defineConfig({
    plugins: [viteSingleFile()],
    build: {
        target: "esnext",
        cssCodeSplit: false,
        assetsInlineLimit: 100000000,
    },
});
