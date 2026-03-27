// Refresh Airtable iframe to prevent stale crashes
document.addEventListener("DOMContentLoaded", function () {
    const iframe = document.getElementById("airtable-form");
    if (!iframe) return;

    const src = iframe.src;
    let wasVisible = false;

    const observer = new IntersectionObserver(
        (entries) => {
            const isVisible = entries[0].isIntersecting;
            if (isVisible && !wasVisible) {
                iframe.src = src;
            }
            wasVisible = isVisible;
        },
        { threshold: 0.1 }
    );

    observer.observe(iframe);
});
