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
                if (data.status === "success") {
                    this.remove();
                    updateTaskStatus(data, form);
                    checkLessonCompletion(lessonId, csrfToken);
                } else {
                    throw new Error(data.message);
                }
            })
            .catch((error) => {
                console.error(error);
                showToast(error, 3000);
            });
        });
    });
});

function updateTaskStatus(data, form) {
    console.log('Data received:', data);

    const highlight = (ids, className) => {
        ids.forEach(id => {
            const input = form.querySelector(`input[value="${id}"]`);
            input?.closest('.lesson-task-answer')?.classList.add(className);
        });
    };

    highlight(data.correct_chosen || [], 'lesson-task-correct');
    highlight(data.incorrect_chosen || [], 'lesson-task-incorrect');
    highlight(data.correct_not_chosen || [], 'lesson-task-correct-not-chosen');
    highlight(data.incorrect_not_chosen || [], 'lesson-task-incorrect-not-chosen');

    form.querySelectorAll(".lesson-task-answer input[type='checkbox'], .lesson-task-answer input[type='radio']")
        .forEach(input => input.disabled = true);
}

