/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'nike-orange': '#FF6B35',
        'chatgpt': {
          'bg': '#343541',
          'user': '#444654',
          'assistant': '#343541',
        }
      }
    },
  },
  plugins: [],
}

