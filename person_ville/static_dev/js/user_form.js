function togglePassword(inputId, button) {
    const input = document.getElementById(inputId);
    const svg = button.querySelector("svg");

    if (!input) {
        return;
    }

    if (input.type === "password") {
        input.type = "text";
        button.setAttribute("aria-label", "Скрыть пароль");
        button.setAttribute("title", "Скрыть пароль");
        svg.innerHTML = `
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M3.98 8.223A10.477 10.477 0 0 0 1.934 11.714
                   a1.012 1.012 0 0 0 0 .572
                   C3.306 16.263 7.243 19.5 12 19.5
                   c2.273 0 4.318-.74 6.02-1.977
                   M6.228 6.228A10.451 10.451 0 0 1 12 4.5
                   c4.757 0 8.694 3.237 10.066 7.214
                   a1.012 1.012 0 0 1 0 .572
                   10.489 10.489 0 0 1-1.285 2.31
                   M6.228 6.228 3 3m3.228 3.228 3.65 3.65
                   m7.894 7.894L21 21m-3.228-3.228-3.65-3.65
                   m0 0a3 3 0 1 1-4.243-4.243m4.242 4.242L9.88 9.88"
            />
        `;
    } else {
        input.type = "password";
        button.setAttribute("aria-label", "Показать пароль");
        button.setAttribute("title", "Показать пароль");
        svg.innerHTML = `
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M2.036 12.322a1.012 1.012 0 0 1 0-.644
                   C3.423 7.51 7.36 4.5 12 4.5
                   c4.638 0 8.573 3.007 9.963 7.178
                   .07.207.07.431 0 .644
                   C20.577 16.49 16.64 19.5 12 19.5
                   c-4.638 0-8.573-3.007-9.964-7.178Z"
            />
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M15 12a3 3 0 1 1-6 0
                   3 3 0 0 1 6 0Z"
            />
        `;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.password-toggle');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const inputId = this.dataset.fieldId;
            if (inputId) {
                togglePassword(inputId, this);
            }
        });
    });
});