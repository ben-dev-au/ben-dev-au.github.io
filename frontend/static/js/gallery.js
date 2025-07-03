// Image Gallery functionality
document.addEventListener("DOMContentLoaded", function () {
    // Initialise the modal with image and title
    var imageModal = document.getElementById("imageModal");
    if (imageModal) {
        imageModal.addEventListener("show.bs.modal", function (event) {
            var triggerElement = event.relatedTarget; // Element that triggered the modal
            var imageSrc = triggerElement.getAttribute("data-bs-image");
            var imageTitle = triggerElement.getAttribute("data-bs-title");

            // Update the modal's content
            var modalTitle = imageModal.querySelector(".modal-title");
            var modalImage = imageModal.querySelector("#modalImage");

            modalTitle.textContent = imageTitle;
            modalImage.src = imageSrc;
            modalImage.alt = imageTitle;
        });
    }
});
