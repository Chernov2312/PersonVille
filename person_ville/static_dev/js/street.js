function validateHouseAnswer() {
    const selected = document.querySelector(
        '.question-board input[name="answer"]:checked'
    );

    if (!selected) {
        alert('Выберите вариант ответа');
        return false;
    }

    return true;
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('houseAnswerForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateHouseAnswer()) {
                e.preventDefault();
            }
        });
    }
});

