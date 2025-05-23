document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".enroll-button").forEach((button) => {
        button.addEventListener("click", function (event) {
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
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Ошибка при обработке запроса');
                }
            })
            .then(data => {
                if (data.status === "success") {
                    showToast('Вы успешно записались на курс', 3000)
                    let message = document.createElement("p");
                    message.classList.add("course-description");
                    message.textContent = "Вы подписаны";
                    form.replaceWith(message);

                    let lockedLesson = document.querySelector(".lesson.locked");
                    let lessonLink = document.querySelector(".lesson-link.hidden");

                    if (lockedLesson && lessonLink) {
                        lockedLesson.remove();
                        lessonLink.classList.remove("hidden");
                    }
                } else {
                    alert("Ошибка: " + data.message);
                }
            })
            .catch((error) => {
                console.error("Ошибка:", error);
                alert("Произошла ошибка при отправке запроса");
            });
        });
    });
});
