function showIncompleteCityAlert() {
    alert(
        'Пока рано фиксировать город.\n\n' +
        'Сначала закройте тесты у всех домиков'
    );
}

function confirmFinalizeCity() {
    return confirm(
        'Вы уверены, что хотите зафиксировать город?\n\n' +
        'После этого вы больше не сможете изменить ответы улиц'
    );
}

function showCharacterUnavailableAlert() {
    alert(
        'Итоговая карточка пока недоступна.\n\n' +
        'Сначала завершите все домики и зафиксируйте город.'
    );
}