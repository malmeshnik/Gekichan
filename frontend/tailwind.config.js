/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0B1120',
        card: '#111827',
        primary: {
          start: '#3B82F6',
          end: '#6366F1',
        },
        text: {
          primary: '#F9FAFB',
          secondary: '#9CA3AF',
        },
        border: '#1F2937',
      },
      spacing: {
        '2xs': '4px',
        'xs': '8px',
        'sm': '12px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        '2xl': '48px',
      },
      backgroundImage: {
        'primary-gradient': 'linear-gradient(to right, #3B82F6, #6366F1)',
      }
    },
  },
  plugins: [],
}
