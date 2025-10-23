/** @type {import('tailwindcss').Config} */
const config = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        primary: ['Quicksand', 'sans-serif'],
        display: ['"Cinzel Decorative"', 'serif'],
      },
      colors: {
        primary: 'rgb(var(--color-primary) / <alpha-value>)',
        secondary: 'rgb(var(--color-secondary) / <alpha-value>)',
        accent: 'rgb(var(--color-accent) / <alpha-value>)',
        bg: {
          DEFAULT: 'rgb(var(--color-bg) / <alpha-value>)',
          secondary: 'rgb(var(--color-bg-secondary) / <alpha-value>)',
          tertiary: 'rgb(var(--color-bg-tertiary) / <alpha-value>)',
        }
      },
      backgroundImage: {
        'gradient-cosmic': 'linear-gradient(45deg, var(--color-bg), var(--color-bg-secondary), var(--color-bg-tertiary))',
      },
      animation: {
        float: 'float 3s ease-in-out infinite',
        pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
}

module.exports = config