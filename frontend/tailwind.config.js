export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        arsenal: {
          red: "#D61F26",
          deep: "#A50E12",
          light: "#FDEBEC",
          gray: "#F5F6F8"
        }
      },
      fontFamily: {
        display: ["Bebas Neue", "sans-serif"],
        body: ["Source Sans 3", "sans-serif"]
      },
      boxShadow: {
        soft: "0 12px 30px rgba(0,0,0,0.08)"
      }
    }
  },
  plugins: []
};
