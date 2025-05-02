document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".submit-button").forEach((button) =>
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
                    showReviewOnPage(data);
                    showToast(data.message);
                } else {
                    let message = "";

                    if (typeof data.errors === 'string') {
                        message = data.errors; // Если это уже строка ошибки — просто юзаем
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
                showToast("Произошла ошибка: " + error.message);
            });
        })
    );
});

function showReviewOnPage(data) {
    if (data.status !== "success" || !data.review) return;

    const reviewsContainer = document.querySelector('.reviews');
    if (!reviewsContainer) return;

    const reviewDiv = document.createElement('div');
    reviewDiv.classList.add('review');

    const reviewHeader = document.createElement('div');
    reviewHeader.classList.add('review-header');

    const userSpan = document.createElement('span');
    userSpan.classList.add('review-user');
    userSpan.textContent = data.review.username;

    const dateSpan = document.createElement('span');
    dateSpan.classList.add('review-date');
    dateSpan.textContent = 'Только что';

    reviewHeader.appendChild(userSpan);
    reviewHeader.appendChild(dateSpan);

    const reviewText = document.createElement('p');
    reviewText.classList.add('review-text');
    reviewText.textContent = data.review.text;

    const reviewRating = document.createElement('p');
    reviewRating.classList.add('review-rating');
    reviewRating.textContent = `⭐ ${data.review.rating}/10`;

    reviewDiv.appendChild(reviewHeader);
    reviewDiv.appendChild(reviewText);
    reviewDiv.appendChild(reviewRating);

    reviewsContainer.insertBefore(reviewDiv, reviewsContainer.firstChild);

    const form = document.querySelector(".review-form");
    if (form) form.reset();
}


