import {checkLessonCompletion} from "./lesson_completion.js";
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".send-button").forEach((button) => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            let lessonId = this.getAttribute("data-lesson-id")
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
                if (data.success) {
                    this.remove();
                    updateTaskStatus(data, form);
                    checkLessonCompletion(lessonId);
                } else {
                    throw new Error("Ошибка: " + data.message);
                }
            })
            .catch((error) => {
                console.error("Ошибка:", error);
                alert("Произошла ошибка при отправке запроса");
            });
        });
    });
});

function updateTaskStatus(data, form) {
    data.correct_chosen.forEach(correctId => {
        document.querySelector(`input[value="${correctId}"]`)
            ?.closest('.lesson-task-answer')
            ?.classList.add('lesson-task-correct');
    });

    data.incorrect_chosen.forEach(incorrectId => {
        document.querySelector(`input[value="${incorrectId}"]`)
            ?.closest('.lesson-task-answer')
            ?.classList.add('lesson-task-incorrect');
    });

    data.correct_not_chosen.forEach(correctId => {
        document.querySelector(`input[value="${correctId}"]`)
            ?.closest('.lesson-task-answer')
            ?.classList.add('lesson-task-correct-not-chosen');
    });

    data.incorrect_not_chosen.forEach(incorrectId => {
        document.querySelector(`input[value="${incorrectId}"]`)
            ?.closest('.lesson-task-answer')
            ?.classList.add('lesson-task-incorrect-not-chosen');
    });
    form.querySelectorAll(".lesson-task-answer input[type='checkbox']").forEach(checkbox => {
        checkbox.disabled = true;
    });
}
