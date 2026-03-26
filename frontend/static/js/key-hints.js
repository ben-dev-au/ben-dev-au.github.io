// Keyboard Shortcut Hints — context-aware animated hint system
document.addEventListener("DOMContentLoaded", function () {
    // Skip on touch-only devices (CSS also hides, this is belt-and-suspenders)
    if (
        "ontouchstart" in window &&
        !window.matchMedia("(pointer: fine)").matches
    ) {
        return;
    }

    var container = document.getElementById("keyHints");
    if (!container) return;

    var hints = container.querySelectorAll(".key-hints__hint");
    var toggle = document.getElementById("keyHintsToggle");
    var overlay = document.getElementById("lightboxOverlay");

    var dismissTimer = null;

    // Track which hints have already been shown this session
    var shownNav = false;
    var shownTimeline = false;

    // --- Helpers ---

    function showHints(hintNames) {
        hints.forEach(function (h) {
            var name = h.getAttribute("data-hint");
            if (hintNames.indexOf(name) >= 0) {
                h.classList.add("key-hints__hint--visible");
            } else {
                h.classList.remove("key-hints__hint--visible");
            }
        });
        if (toggle) toggle.classList.remove("key-hints__toggle--visible");
    }

    function hideAllHints() {
        hints.forEach(function (h) {
            h.classList.remove("key-hints__hint--visible");
        });
        if (toggle) toggle.classList.add("key-hints__toggle--visible");
    }

    function showForDuration(hintNames, ms) {
        clearTimeout(dismissTimer);
        showHints(hintNames);
        dismissTimer = setTimeout(hideAllHints, ms || 3500);
    }

    // --- Context helpers ---

    function isLightboxOpen() {
        return overlay && overlay.classList.contains("active");
    }

    function isLightboxGallery() {
        return overlay && overlay.classList.contains("has-gallery");
    }

    // --- Section detection (track first visit to timeline) ---

    var resumeSection = document.getElementById("resume-section");

    if (resumeSection && window.IntersectionObserver) {
        var obs = new IntersectionObserver(
            function (entries) {
                if (entries[0].isIntersecting && !shownTimeline && !isLightboxOpen()) {
                    shownTimeline = true;
                    showForDuration(["slides", "enter"], 4000);
                }
            },
            { threshold: 0.3 }
        );
        obs.observe(resumeSection);
    }

    // --- Lightbox detection via MutationObserver ---

    function onLightboxClose() {
        container.classList.remove("key-hints--lightbox");
        clearTimeout(dismissTimer);
        hideAllHints();
    }

    if (overlay && window.MutationObserver) {
        var lightboxObs = new MutationObserver(function () {
            if (isLightboxOpen()) {
                container.classList.add("key-hints--lightbox");
                clearTimeout(dismissTimer);
                var lbHints = ["close"];
                if (isLightboxGallery()) lbHints.push("gallery");
                showHints(lbHints);
            } else {
                onLightboxClose();
            }
        });
        lightboxObs.observe(overlay, {
            attributes: true,
            attributeFilter: ["class"],
        });
    }

    // Direct listeners for mouse-close (belt-and-suspenders with MutationObserver)
    var lightboxClose = document.getElementById("lightboxClose");
    if (lightboxClose) {
        lightboxClose.addEventListener("click", onLightboxClose);
    }
    if (overlay) {
        overlay.addEventListener("click", function (e) {
            if (e.target === overlay) onLightboxClose();
        });
    }

    // --- Toggle button ---

    if (toggle) {
        toggle.addEventListener("click", function () {
            if (isLightboxOpen()) {
                var lbHints = ["close"];
                if (isLightboxGallery()) lbHints.push("gallery");
                showForDuration(lbHints, 5000);
            } else if (resumeSection) {
                var rect = resumeSection.getBoundingClientRect();
                var inTimeline = rect.top < window.innerHeight && rect.bottom > 0;
                if (inTimeline) {
                    showForDuration(["nav", "slides", "enter"], 5000);
                } else {
                    showForDuration(["nav"], 5000);
                }
            } else {
                showForDuration(["nav"], 5000);
            }
        });
    }

    // --- First visit: show nav hints once, then idle ---

    if (!shownNav) {
        shownNav = true;
        setTimeout(function () {
            showForDuration(["nav"], 5000);
        }, 1500);
    }
});
