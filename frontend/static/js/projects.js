// Featured Project — open the hero image in the shared lightbox
document.addEventListener("DOMContentLoaded", function () {
    var trigger = document.querySelector(".featured-image");
    var overlay = document.getElementById("lightboxOverlay");
    if (!trigger || !overlay) return;

    var img = trigger.querySelector("img");
    if (!img) return;

    var lightboxImage = document.getElementById("lightboxImage");
    var lightboxCaption = document.getElementById("lightboxCaption");

    function openLightbox() {
        lightboxImage.src = img.src;
        lightboxImage.alt = img.alt;
        lightboxCaption.textContent = img.alt;
        // Single image — clearing has-gallery keeps the prev/next arrows hidden
        overlay.classList.remove("has-gallery");
        overlay.classList.add("active");
    }

    trigger.addEventListener("click", openLightbox);

    trigger.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            openLightbox();
        }
    });

    // timeline.js owns close/nav on the shared overlay, but it bails early when
    // there is no timeline on the page — cover closing ourselves in that case so
    // the overlay can never trap the viewer.
    if (document.getElementById("timelineSwiper")) return;

    function closeLightbox() {
        overlay.classList.remove("active", "has-gallery");
    }

    var lightboxClose = document.getElementById("lightboxClose");
    if (lightboxClose) {
        lightboxClose.addEventListener("click", closeLightbox);
    }

    overlay.addEventListener("click", function (e) {
        if (e.target === overlay) closeLightbox();
    });

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") closeLightbox();
    });
});
