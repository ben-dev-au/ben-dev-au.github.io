// Navbar functionality
document.addEventListener("DOMContentLoaded", function () {
    // Navbar scroll behavior
    window.addEventListener("scroll", () => {
        const navToggle = document.querySelector(".navbar-toggler");
        if (window.scrollY > 50) {
            navToggle.classList.add("scrolled");
        } else {
            navToggle.classList.remove("scrolled");
        }
    });

    window.addEventListener("scroll", function () {
        const navbar = document.querySelector(".custom-navbar");
        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });

    // Auto close mobile nav when nav-link is clicked
    document.querySelectorAll(".custom-navbar .nav-link").forEach((link) => {
        link.addEventListener("click", function () {
            const navbarCollapse = document.querySelector(
                ".custom-navbar .navbar-collapse"
            );

            if (navbarCollapse.classList.contains("show")) {
                // Collapse the menu using Bootstrap's Collapse API
                new bootstrap.Collapse(navbarCollapse, {
                    toggle: false,
                }).hide();
            }
        });
    });
});
