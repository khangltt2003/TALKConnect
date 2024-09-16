/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        main: "#0D98BA", // Define your main color here
      },
      fontSize: {
        base: "18px", // or any size you prefer
      },
    },
  },
  plugins: [],
};
