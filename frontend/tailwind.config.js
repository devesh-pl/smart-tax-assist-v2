/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-outfit)', 'sans-serif'],
        mono: ['var(--font-jetbrains)', 'monospace'],
      },
      colors: {
        brand: {
          50:  '#eef6ff',
          100: '#d9eaff',
          200: '#bcd8ff',
          300: '#8dbbff',
          400: '#5794ff',
          500: '#2f6ef7',
          600: '#1a4eec',
          700: '#1339d9',
          800: '#162fb0',
          900: '#172d8a',
          950: '#121e57',
        },
        surface: {
          DEFAULT: '#0f172a',
          card:    '#1e293b',
          border:  '#334155',
          muted:   '#475569',
        },
      },
      animation: {
        'fade-up':   'fadeUp 0.4s ease-out forwards',
        'shimmer':   'shimmer 1.5s infinite',
        'pulse-dot': 'pulseDot 1.2s ease-in-out infinite',
      },
      keyframes: {
        fadeUp: {
          '0%':   { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        shimmer: {
          '0%':   { backgroundPosition: '-400px 0' },
          '100%': { backgroundPosition: '400px 0' },
        },
        pulseDot: {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%':      { opacity: '0.4', transform: 'scale(0.75)' },
        },
      },
    },
  },
  plugins: [],
}
