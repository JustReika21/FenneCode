document.addEventListener("DOMContentLoaded", function () {
    const editors = [];

    document.querySelectorAll(".code-editor").forEach((textarea, index) => {
        const editor = CodeMirror.fromTextArea(textarea, {
            mode: "python",
            lineNumbers: true,
            theme: "darcula"
        });
        editors.push(editor);
    });

    document.querySelectorAll(".run-button").forEach((button, index) => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            const form = button.closest(".code-form");
            const output = form.querySelector(".output");
            const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;
            const code = editors[index].getValue();

            const formData = new FormData();
            formData.append("csrfmiddlewaretoken", csrfToken);
            formData.append("code", code);

            fetch(form.action, {
                method: "POST",
                body: formData,
                credentials: "same-origin"
            })
            .then(async response => {
                const data = await response.json();
                if (!response.ok) throw data;
                output.classList.remove("hidden");
                output.textContent = data.console_output || "Нет вывода.";
            })
            .catch(err => {
                output.textContent = "Ошибка: " + (
                    err.console_output || JSON.stringify(err)
                );
            });
        });
    });

    document.querySelectorAll(".copy-button").forEach((button, index) => {
        button.addEventListener("click", function () {
            navigator.clipboard.writeText(editors[index].getValue())
                .then(() => showToast("Код скопирован!", 3000))
                .catch(() => showToast("Не удалось скопировать код.", 3000));
        });
    });
});
