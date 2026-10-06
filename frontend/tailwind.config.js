/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,html}", // Traccia tutti i file in src
  ],
  theme: {
    extend: {
      colors: {
        'neutral-primary': '#171717', // <-- Cambia con il tuo colore scuro reale
        'default': '#e5e7eb',         // <-- Cambia con il colore del bordo reale
      },
    },
  },
  plugins: [],
}
