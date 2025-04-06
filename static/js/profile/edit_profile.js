document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('.submit-button');
    if (button) {
        button.addEventListener('click',function (event) {
            event.preventDefault();

            let form = this.closest('form');
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
                    this.remove()
                } else {
                    const errors = data.errors || {};
                    const messages = [];

                    for (let field in errors) {
                        if (errors[field].length > 0) {
                            messages.push(errors[field][0]); // 👈 just first error
                        }
                    }

                    alert(messages.join('\n'));
                }
            })
            .catch((error) => {
                console.error("Ошибка:", error);
                alert("Произошла ошибка при отправке запроса: " + error.errors);
            });
        })
    }
})