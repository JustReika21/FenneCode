document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".send-button").forEach((button) => {
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
                if (data.success) {
                    this.remove()
                    let message = document.querySelector("form");
                    data.correct_chosen.forEach(correctId => {
                        let correctLabel = document.querySelector(
                            `input[value="${correctId}"]`
                        )?.closest('.lesson-task-answer');
                        if (correctLabel) {
                            correctLabel.classList.add('lesson-task-correct')
                        }
                    });
                    data.incorrect_chosen.forEach(incorrectId => {
                        let incorrectLabel = document.querySelector(`input[value="${incorrectId}"]`)?.closest('.lesson-task-answer');
                        if (incorrectLabel) {
                            incorrectLabel.classList.add('lesson-task-incorrect')
                        }
                    });
                    data.correct_not_chosen.forEach(incorrectId => {
                        let incorrectLabel = document.querySelector(`input[value="${incorrectId}"]`)?.closest('.lesson-task-answer');
                        if (incorrectLabel) {
                            incorrectLabel.classList.add('lesson-task-correct-not-chosen')
                        }
                    });
                    data.incorrect_not_chosen.forEach(incorrectId => {
                        let incorrectLabel = document.querySelector(`input[value="${incorrectId}"]`)?.closest('.lesson-task-answer');
                        if (incorrectLabel) {
                            incorrectLabel.classList.add('lesson-task-incorrect-not-chosen')
                        }
                    });
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