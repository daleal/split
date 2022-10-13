/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      height: {
        screen: 'calc(var(--vh) * 100)',
      },
    },
  },
  plugins: [],
};
