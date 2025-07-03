// Scroll functionality
document.addEventListener("DOMContentLoaded", function () {
    // Scroll to About Section
    const scrollToAboutBtn = document.getElementById("scrollToAbout");
    if (scrollToAboutBtn) {
        scrollToAboutBtn.addEventListener("click", function (event) {
            event.preventDefault();
            document
                .querySelector("#about-section")
                .scrollIntoView({ behavior: "smooth" });
        });
    }

    // Scroll to Resume Section
    const scrollToResumeBtn = document.getElementById("scrollToResume");
    if (scrollToResumeBtn) {
        scrollToResumeBtn.addEventListener("click", function (event) {
            event.preventDefault();
            document
                .querySelector("#resume-section")
                .scrollIntoView({ behavior: "smooth" });
        });
    }

    // Scroll to Projects Section
    const scrollToProjectsBtn = document.getElementById("scrollToProjects");
    if (scrollToProjectsBtn) {
        scrollToProjectsBtn.addEventListener("click", function (event) {
            event.preventDefault();
            document
                .querySelector("#projects")
                .scrollIntoView({ behavior: "smooth" });
        });
    }

    // Scroll to Footer Section
    const scrollToFooterBtn = document.getElementById("scrollToFooter");
    if (scrollToFooterBtn) {
        scrollToFooterBtn.addEventListener("click", function (event) {
            event.preventDefault();
            document
                .querySelector("#footer")
                .scrollIntoView({ behavior: "smooth" });
        });
    }

    // Scroll to Intro Section from Footer
    const scrollToIntroBtn = document.getElementById("scrollToIntro");
    if (scrollToIntroBtn) {
        scrollToIntroBtn.addEventListener("click", function (event) {
            event.preventDefault();
            document
                .querySelector("#intro")
                .scrollIntoView({ behavior: "smooth" });
        });
    }

    // Scroll to top button functionality
    const scrollBtn = document.getElementById("scrollTopBtn");

    // Show button when scrolled down
    window.addEventListener("scroll", function () {
        scrollBtn.style.display = window.scrollY > 100 ? "block" : "none";
    });

    // Smooth scroll to the top of the page
    scrollBtn.addEventListener("click", function () {
        window.scrollTo({
            top: 0,
            behavior: "smooth",
        });
    });
});
