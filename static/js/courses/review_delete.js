document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".delete-button").forEach((button) =>
        button.addEventListener("click", function(event) {
            event.preventDefault();

            let form = this.closest("form");
            let formData = new FormData(form);
            let csrfToken = formData.get("csrfmiddlewaretoken");
            let url = form.action;

            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Accept": "application/json",
                },
                credentials: "same-origin",
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    removeReviewFromPage(form);
                    showToast(data.message);
                } else {
                    let message = "";

                    if (typeof data.errors === 'string') {
                        message = data.errors;
                    } else if (typeof data.errors === 'object') {
                        for (let key in data.errors) {
                            if (Array.isArray(data.errors[key])) {
                                data.errors[key].forEach(errorObj => {
                                    if (errorObj.message) {
                                        message += `Ошибка: ${errorObj.message}\n`;
                                    }
                                });
                            }
                        }
                    } else {
                        message = "Что-то пошло не так. Ошибки — как призраки, есть, но не видны.";
                    }

                    showToast(message.trim(), 5000);
                }
            })
            .catch((error) => {
                console.error("Ошибка", error);
                showToast("Произошла ошибка: " + error.message, 5000);
            });
        })
    );
});

function removeReviewFromPage(form) {
    const reviewDiv = form.closest('.review');
    const reviewsContainer = document.querySelector('.reviews');

    if (reviewDiv) reviewDiv.remove();

    if (reviewsContainer && reviewsContainer.querySelectorAll('.review').length === 0) {
        const noReviewsMessage = document.createElement('p');
        noReviewsMessage.className = 'no-reviews';
        noReviewsMessage.textContent = 'Пока отзывов нет. Будьте первым!';
        reviewsContainer.appendChild(noReviewsMessage);
    }
}