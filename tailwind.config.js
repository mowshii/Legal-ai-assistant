/**
 * tailwind.config.js
 * --------------------
 * Design tokens grounded in the subject matter: aged legal paper, ink,
 * and a wax-seal accent — a legal-document-intelligence palette rather
 * than a generic SaaS-purple one.
 *
 *   ink        #2B1B12  — headings, primary text
 *   manuscript #6B3F22  — brand/primary actions, nav
 *   seal       #B5502F  — CTA accent, HIGH risk, the one bold color
 *   parchment  #F3E9D8  — page background
 *   paper      #FFFCF6  — card background
 *   moss       #6E7B52  — LOW risk / success
 *   ochre      #C08A28  — MEDIUM risk
 */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#2B1B12",
        manuscript: {
          DEFAULT: "#6B3F22",
          light: "#8C5A34",
          dark: "#4A2B16",
        },
        seal: {
          DEFAULT: "#B5502F",
          light: "#CD6B48",
        },
        parchment: "#F3E9D8",
        paper: "#FFFCF6",
        moss: "#6E7B52",
        ochre: "#C08A28",
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        body: ["Catamaran", "sans-serif"],
      },
      boxShadow: {
        paper: "0 1px 0 rgba(43,27,18,0.06), 0 8px 24px rgba(43,27,18,0.08)",
      },
    },
  },
  plugins: [],
};
