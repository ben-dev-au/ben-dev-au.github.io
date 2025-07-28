// Scroll functionality
document.addEventListener("DOMContentLoaded", function () {
    const sections = ["intro", "about-section", "resume-section", "projects", "footer"];
    let currentSectionIndex = 0;
    let isScrolling = false;

    function scrollToSection(index) {
        if (isScrolling) return;
        if (index >= 0 && index < sections.length) {
            const sectionId = sections[index];
            const section = document.getElementById(sectionId);
            if (section) {
                isScrolling = true;
                currentSectionIndex = index;
                window.scrollTo({
                    top: section.offsetTop,
                    behavior: "smooth",
                });
                setTimeout(() => {
                    isScrolling = false;
                }, 1000);
            }
        }
    }

    document.addEventListener("keydown", function (event) {
        if (event.key === "ArrowDown") {
            event.preventDefault();
            if (currentSectionIndex < sections.length - 1) {
                scrollToSection(currentSectionIndex + 1);
            }
        } else if (event.key === "ArrowUp") {
            event.preventDefault();
            if (currentSectionIndex > 0) {
                scrollToSection(currentSectionIndex - 1);
            }
        }
    });

    // Scroll to About Section
    const scrollToAboutBtn = document.getElementById("scrollToAbout");
    if (scrollToAboutBtn) {
        scrollToAboutBtn.addEventListener("click", function (event) {
            event.preventDefault();
            scrollToSection(1);
        });
    }

    // Scroll to Resume Section
    const scrollToResumeBtn = document.getElementById("scrollToResume");
    if (scrollToResumeBtn) {
        scrollToResumeBtn.addEventListener("click", function (event) {
            event.preventDefault();
            scrollToSection(2);
        });
    }

    // Scroll to Projects Section
    const scrollToProjectsBtn = document.getElementById("scrollToProjects");
    if (scrollToProjectsBtn) {
        scrollToProjectsBtn.addEventListener("click", function (event) {
            event.preventDefault();
            scrollToSection(3);
        });
    }

    // Scroll to Footer Section
    const scrollToFooterBtn = document.getElementById("scrollToFooter");
    if (scrollToFooterBtn) {
        scrollToFooterBtn.addEventListener("click", function (event) {
            event.preventDefault();
            scrollToSection(4);
        });
    }

    // Scroll to Intro Section from Footer
    const scrollToIntroBtn = document.getElementById("scrollToIntro");
    if (scrollToIntroBtn) {
        scrollToIntroBtn.addEventListener("click", function (event) {
            event.preventDefault();
            scrollToSection(0);
        });
    }

    // Scroll to top button functionality
    const scrollBtn = document.getElementById("scrollTopBtn");

    // Show button when scrolled down
    window.addEventListener("scroll", function () {
        if (!isScrolling) {
            const scrollPosition = window.scrollY + window.innerHeight / 2;
            let newCurrentSectionIndex = 0;
            for (let i = 0; i < sections.length; i++) {
                const section = document.getElementById(sections[i]);
                if (section && section.offsetTop <= scrollPosition) {
                    newCurrentSectionIndex = i;
                }
            }
            currentSectionIndex = newCurrentSectionIndex;
        }
        scrollBtn.style.display = window.scrollY > 100 ? "block" : "none";
    });

    // Smooth scroll to the top of the page
    scrollBtn.addEventListener("click", function () {
        scrollToSection(0);
    });
});
