document.addEventListener("DOMContentLoaded", function () {
    const editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        mode: "python",
        lineNumbers: true,
        theme: "default"
    });

    window.runCode = function (event) {
        event.preventDefault();

        const form = document.getElementById("code-form");
        const output = document.getElementById("output");
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', form.querySelector('[name=csrfmiddlewaretoken]').value);
        formData.append('code', editor.getValue());

        fetch(form.action, {
            method: 'POST',
            body: formData,
            credentials: "same-origin"
        })
        .then(async response => {
            const data = await response.json();
            if (!response.ok) {
                throw data;
            }
            output.textContent = data.console_output;
        })
        .catch(err => {
            output.textContent = "Ошибка: " + (
                err.console_output || JSON.stringify(err)
            );
        });
    };


    window.copyCode = function () {
        navigator.clipboard.writeText(editor.getValue())
            .then(() => showToast("Код скопирован!"), 3000)
            .catch(() => showToast("Не удалось скопировать код.", 3000));
    };
});