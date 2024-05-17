/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'primary-50': '#E7EDFF',
        'primary-100': '#BDCCFF',
        'primary-200': '#93ABFF',
        'primary-300': '#698AFF',
        'primary-400': '#3F6AFF',
        'primary-500': '#1447F8',
        'primary-600': '#012FCF',
        'primary-700': '#0025A6',
        'primary-800': '#001C7E',
        'primary-900': '#001355'
      }
    }
  },
  plugins: []
}
