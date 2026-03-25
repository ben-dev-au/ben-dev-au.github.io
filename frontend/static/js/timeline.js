// Timeline Swiper — Horizontal career milestones + Lightbox + Image rotation
document.addEventListener("DOMContentLoaded", function () {
    var swiperEl = document.getElementById("timelineSwiper");
    if (!swiperEl) return;

    var slides = swiperEl.querySelectorAll(".swiper-slide");
    var paginationContainer = document.getElementById("timelinePagination");
    var progressBar = document.getElementById("timelineProgressBar");
    var totalSlides = slides.length;

    // Build year dot pagination
    var dots = [];
    slides.forEach(function (slide, index) {
        var yearShort = slide.getAttribute("data-year-short") || slide.getAttribute("data-year") || "";
        var dot = document.createElement("div");
        dot.className = "timeline-dot" + (index === 0 ? " active" : "");
        dot.innerHTML =
            '<div class="timeline-dot-circle"></div>' +
            '<span class="timeline-dot-year">' + yearShort + "</span>";
        dot.addEventListener("click", function () {
            swiper.slideTo(index);
        });
        paginationContainer.appendChild(dot);
        dots.push(dot);
    });

    function updatePagination(activeIndex) {
        dots.forEach(function (dot, i) {
            dot.classList.toggle("active", i === activeIndex);
        });
        var progress = totalSlides > 1 ? (activeIndex / (totalSlides - 1)) * 100 : 0;
        progressBar.style.width = progress + "%";
    }

    var swiper = new Swiper("#timelineSwiper", {
        direction: "horizontal",
        slidesPerView: 1,
        centeredSlides: true,
        grabCursor: true,
        speed: 500,
        spaceBetween: 24,
        mousewheel: false,
        keyboard: false,
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        breakpoints: {
            768: {
                slidesPerView: 2,
                spaceBetween: 28,
            },
            1024: {
                slidesPerView: 3,
                spaceBetween: 32,
            },
        },
        on: {
            slideChange: function () {
                updatePagination(this.activeIndex);
            },
        },
    });

    updatePagination(0);

    // Keyboard navigation — arrow keys control the timeline when the section is in view
    var resumeSection = document.getElementById("resume-section");
    var timelineInView = false;

    if (resumeSection && window.IntersectionObserver) {
        var observer = new IntersectionObserver(function (entries) {
            timelineInView = entries[0].isIntersecting;
        }, { threshold: 0.3 });
        observer.observe(resumeSection);
    }

    document.addEventListener("keydown", function (e) {
        if (!timelineInView) return;
        if (overlay && overlay.classList.contains("active")) return;
        if (e.key === "ArrowLeft") {
            e.preventDefault();
            swiper.slidePrev();
        } else if (e.key === "ArrowRight") {
            e.preventDefault();
            swiper.slideNext();
        } else if (e.key === "Enter") {
            e.preventDefault();
            var activeSlide = swiper.slides[swiper.activeIndex];
            if (activeSlide) {
                var photo = activeSlide.querySelector(".polaroid-photo");
                if (photo) photo.click();
            }
        }
    });

    // Rotating images — crossfade between multiple images
    var rotatingCards = document.querySelectorAll(".polaroid-card[data-images]");
    rotatingCards.forEach(function (card) {
        var images = card.querySelectorAll(".polaroid-rotate");
        var captions = (card.getAttribute("data-captions") || "").split(",");
        var label = card.querySelector(".polaroid-label");
        if (images.length < 2) return;

        var currentIndex = 0;
        setInterval(function () {
            images[currentIndex].classList.remove("active");
            currentIndex = (currentIndex + 1) % images.length;
            images[currentIndex].classList.add("active");
            if (label && captions[currentIndex]) {
                label.textContent = captions[currentIndex].trim();
            }
            card.setAttribute("data-caption", (captions[currentIndex] || "").trim());
        }, 4000);
    });

    // Lightbox
    var overlay = document.getElementById("lightboxOverlay");
    var lightboxImage = document.getElementById("lightboxImage");
    var lightboxCaption = document.getElementById("lightboxCaption");
    var lightboxClose = document.getElementById("lightboxClose");
    var lightboxPrev = document.getElementById("lightboxPrev");
    var lightboxNext = document.getElementById("lightboxNext");

    if (!overlay) return;

    // Gallery state for multi-image cards
    var galleryImages = [];
    var galleryCaptions = [];
    var galleryIndex = 0;

    function showGalleryImage(index) {
        galleryIndex = index;
        lightboxImage.src = galleryImages[index];
        lightboxImage.alt = galleryCaptions[index] || "";
        lightboxCaption.textContent = galleryCaptions[index] || "";
    }

    // Click photo area to open lightbox
    var photos = document.querySelectorAll(".polaroid-photo");
    photos.forEach(function (photo) {
        var card = photo.closest(".polaroid-card");
        photo.addEventListener("click", function (e) {
            if (e.defaultPrevented) return;

            var imagesAttr = card ? card.getAttribute("data-images") : null;
            var captionsAttr = card ? card.getAttribute("data-captions") : null;

            if (imagesAttr) {
                // Multi-image card — build gallery
                galleryImages = imagesAttr.split(",").map(function (s) { return s.trim(); });
                galleryCaptions = captionsAttr ? captionsAttr.split(",").map(function (s) { return s.trim(); }) : [];
                // Start on whichever image is currently active
                var activeImg = photo.querySelector(".polaroid-rotate.active");
                var startIndex = activeImg ? galleryImages.indexOf(activeImg.src) : 0;
                if (startIndex < 0) startIndex = 0;
                overlay.classList.add("active", "has-gallery");
                showGalleryImage(startIndex);
            } else {
                // Single-image card
                galleryImages = [];
                galleryCaptions = [];
                overlay.classList.add("active");
                overlay.classList.remove("has-gallery");
                var img = photo.querySelector("img");
                var caption = card ? (card.getAttribute("data-caption") || "") : "";
                if (img) {
                    lightboxImage.src = img.src;
                    lightboxImage.alt = img.alt;
                    lightboxCaption.textContent = caption;
                }
            }
        });
    });

    function navigateGallery(direction) {
        if (galleryImages.length < 2) return;
        var next = (galleryIndex + direction + galleryImages.length) % galleryImages.length;
        showGalleryImage(next);
    }

    if (lightboxPrev) {
        lightboxPrev.addEventListener("click", function (e) {
            e.stopPropagation();
            navigateGallery(-1);
        });
    }

    if (lightboxNext) {
        lightboxNext.addEventListener("click", function (e) {
            e.stopPropagation();
            navigateGallery(1);
        });
    }

    function closeLightbox() {
        overlay.classList.remove("active", "has-gallery");
    }

    if (lightboxClose) {
        lightboxClose.addEventListener("click", closeLightbox);
    }

    overlay.addEventListener("click", function (e) {
        if (e.target === overlay) closeLightbox();
    });

    document.addEventListener("keydown", function (e) {
        if (!overlay.classList.contains("active")) return;
        if (e.key === "Escape") closeLightbox();
        if (e.key === "ArrowLeft") navigateGallery(-1);
        if (e.key === "ArrowRight") navigateGallery(1);
    });
});
