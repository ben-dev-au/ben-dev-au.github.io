// Polaroid Gallery — Drag interaction + Custom Lightbox
document.addEventListener("DOMContentLoaded", function () {
    var gallery = document.getElementById("polaroidGallery");
    var polaroids = gallery ? gallery.querySelectorAll(".polaroid") : [];
    var overlay = document.getElementById("lightboxOverlay");
    var lightboxImage = document.getElementById("lightboxImage");
    var lightboxCaption = document.getElementById("lightboxCaption");
    var lightboxClose = document.getElementById("lightboxClose");

    var isMobile = window.matchMedia("(max-width: 992px)").matches;
    var dragState = null;
    var hasDragged = false;

    // Desktop: drag polaroids
    if (!isMobile) {
        polaroids.forEach(function (polaroid) {
            polaroid.addEventListener("mousedown", function (e) {
                if (e.button !== 0) return;
                e.preventDefault();
                hasDragged = false;

                var rect = polaroid.getBoundingClientRect();
                var galleryRect = gallery.getBoundingClientRect();

                dragState = {
                    el: polaroid,
                    offsetX: e.clientX - rect.left,
                    offsetY: e.clientY - rect.top,
                    galleryLeft: galleryRect.left,
                    galleryTop: galleryRect.top,
                };

                polaroid.classList.add("is-dragging");
            });
        });

        document.addEventListener("mousemove", function (e) {
            if (!dragState) return;
            hasDragged = true;

            var newX = e.clientX - dragState.galleryLeft - dragState.offsetX;
            var newY = e.clientY - dragState.galleryTop - dragState.offsetY;

            dragState.el.style.left = newX + "px";
            dragState.el.style.top = newY + "px";
            dragState.el.style.setProperty("--x", "unset");
            dragState.el.style.setProperty("--y", "unset");
        });

        document.addEventListener("mouseup", function () {
            if (dragState) {
                dragState.el.classList.remove("is-dragging");
                dragState = null;
            }
        });
    }

    // Click/tap to open lightbox
    polaroids.forEach(function (polaroid) {
        polaroid.addEventListener("click", function () {
            if (hasDragged) {
                hasDragged = false;
                return;
            }
            var img = polaroid.querySelector("img");
            var caption = polaroid.getAttribute("data-caption") || "";
            if (img && overlay) {
                lightboxImage.src = img.src;
                lightboxImage.alt = img.alt;
                lightboxCaption.textContent = caption;
                overlay.classList.add("active");
            }
        });
    });

    // Close lightbox
    function closeLightbox() {
        if (overlay) {
            overlay.classList.remove("active");
        }
    }

    if (lightboxClose) {
        lightboxClose.addEventListener("click", closeLightbox);
    }

    if (overlay) {
        overlay.addEventListener("click", function (e) {
            if (e.target === overlay) {
                closeLightbox();
            }
        });
    }

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            closeLightbox();
        }
    });
});
