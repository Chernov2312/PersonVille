function confirmLogout(hasCityResult) {
    if (hasCityResult) {
        return confirm(
            "Вы уверены, что хотите выйти?\n\nТекущий город будет сброшен"
        );
    }
    return confirm("Вы уверены, что хотите выйти из аккаунта?");
}

function openCharacterFromHeader(event) {
    if (event) {
        event.preventDefault();
    }
    
    if (typeof openCharacterModal === "function") {
        openCharacterModal();
        return false;
    }
    const characterUrl = document.querySelector('[data-character-url]')?.dataset.characterUrl || '/city/';
    window.location.href = characterUrl;
    return false;
}