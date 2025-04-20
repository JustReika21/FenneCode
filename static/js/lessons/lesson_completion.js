export function checkLessonCompletion(lessonId, csrfToken) {
    fetch(`/api/check_lesson_completion/${lessonId}`)
        .then(response => response.json())
        .then(data => {
            if (data.is_all_tasks_completed) {
                fetch(`/api/mark_lesson_complete/${lessonId}`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json',
                    },
                    credentials: "same-origin",
                })
                .then(markResponse => {
                    if (!markResponse.ok) {
                        return;
                    }

                    const nextLessonButton = document.querySelector(".lesson-nav-button.next");
                    const nextLessonUrl = nextLessonButton?.getAttribute("data-next-lesson-url");

                    if (nextLessonUrl) {
                        nextLessonButton.setAttribute("href", nextLessonUrl);
                    }
                });
            }
        })
        .catch(error => {
            console.error("Ошибка при проверке статуса урока:", error);
        });
}