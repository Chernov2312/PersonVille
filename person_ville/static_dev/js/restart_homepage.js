function handleTestStart(hasCityResult, firstUrl, restartUrl) {
    if (!hasCityResult) {
        window.location.href = firstUrl + "?reset=1";
        return false;
    }

    const restart = confirm(
        "Тест уже пройден.\n\nНажмите Да, чтобы начать заново.\nНажмите Нет, чтобы остаться"
    );

    if (restart) {
        fetch(restartUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else if (response.ok) {
                window.location.href = restartUrl;
            } else {
                window.location.href = restartUrl;
            }
        }).catch(error => {
            console.error('Error:', error);
            window.location.href = restartUrl;
        });
    }

    return false;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}