// Timeline Swiper — Horizontal career milestones
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
        var year = slide.getAttribute("data-year") || "";
        var dot = document.createElement("div");
        dot.className = "timeline-dot" + (index === 0 ? " active" : "");
        dot.innerHTML =
            '<div class="timeline-dot-circle"></div>' +
            '<span class="timeline-dot-year">' + year + "</span>";
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
        // Update progress bar
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

    // Set initial progress
    updatePagination(0);
});
