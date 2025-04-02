export function checkLessonCompletion(lessonId) {
    fetch(`/api/check_lesson_completion/${lessonId}`)
        .then(response => response.json())
        .then(completionData => {
            if (completionData.is_all_tasks_completed) {
                let nextLessonButton = document.querySelector(".lesson-nav-button.next");
                let nextLessonUrl = nextLessonButton.getAttribute("data-next-lesson-url");

                if (nextLessonUrl) {
                    nextLessonButton.setAttribute("href", nextLessonUrl);
                }
            }
        })
        .catch(error => {
            console.error("Ошибка при проверке статуса урока:", error);
        });
}
