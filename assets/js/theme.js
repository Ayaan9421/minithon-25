document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("theme-toggle");
  const savedTheme = localStorage.getItem("theme");

  // Page load → apply saved theme
  if (savedTheme === "dark") {
    document.documentElement.classList.add("dark");
    if (toggle) toggle.checked = true;
  } else {
    document.documentElement.classList.remove("dark");
    if (toggle) toggle.checked = false;
  }

  // Agar toggle present hai (sirf settings page pe) to event bind karo
  if (toggle) {
    toggle.addEventListener("change", () => {
      if (toggle.checked) {
        document.documentElement.classList.add("dark");
        localStorage.setItem("theme", "dark");
      } else {
        document.documentElement.classList.remove("dark");
        localStorage.setItem("theme", "light");
      }
    });
  }
});