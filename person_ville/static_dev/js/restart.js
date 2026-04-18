function handleTestStart(hasCityResult, firstUrl, restartUrl) {
    if (!hasCityResult) {
        window.location.href = firstUrl + "?reset=1";
        return false;
    }

    const restart = confirm(
        "Тест уже пройден.\n\nНажмите Да, чтобы начать заново.\nНажмите Нет, чтобы вернуться"
    );

    if (restart) {
        window.location.href = restartUrl;
    }

    return false;
}