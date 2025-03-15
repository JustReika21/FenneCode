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
                if (data.status === "ok") {
                    let message = document.createElement("p");
                    message.classList.add("course-description");
                    message.textContent = "Вы подписаны";

                    form.replaceWith(message);
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
