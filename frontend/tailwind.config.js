/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#4F46E5",
        secondary: "#1E1B4B",
        ink: "#0F172A",
        mist: "#F8FAFC",
        line: "#E2E8F0",
      },
      fontFamily: {
        sans: ["Poppins", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      boxShadow: {
        panel: "0 24px 60px rgba(15, 23, 42, 0.12)",
      },
      backgroundImage: {
        aura: "radial-gradient(circle at top left, rgba(79, 70, 229, 0.22), transparent 34%), radial-gradient(circle at bottom right, rgba(30, 27, 75, 0.16), transparent 30%)",
      },
    },
  },
  plugins: [],
};
