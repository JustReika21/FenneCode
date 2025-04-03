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
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    showReviewOnPage(data)
                } else {
                    throw new Error("Ошибка: " + data.message);
                }
            })
            .catch((error) => {
                console.error("Ошибка", error);
                alert("Произошла ошибка: " + error.message);
            });
        })
    );
});

function showReviewOnPage(data) {
    if (!data.success) return;

    const reviewsContainer = document.querySelector('.reviews');

    const reviewDiv = document.createElement('div');
    reviewDiv.classList.add('review');

    const reviewHeader = document.createElement('div');
    reviewHeader.classList.add('review-header');

    const userSpan = document.createElement('span');
    userSpan.classList.add('review-user');
    userSpan.textContent = data.username;

    const dateSpan = document.createElement('span');
    dateSpan.classList.add('review-date');
    dateSpan.textContent = 'Только что'

    reviewHeader.appendChild(userSpan);
    reviewHeader.appendChild(dateSpan);

    const reviewText = document.createElement('p');
    reviewText.classList.add('review-text');
    reviewText.textContent = `${data.text}`;

    const reviewRating = document.createElement('p');
    reviewRating.classList.add('review-rating');
    reviewRating.textContent = `⭐ ${data.rating}/10`;

    reviewDiv.appendChild(reviewHeader);
    reviewDiv.appendChild(reviewText);
    reviewDiv.appendChild(reviewRating);

    reviewsContainer.insertBefore(reviewDiv, reviewsContainer.firstChild);

    document.querySelector(".review-form").reset();
}

