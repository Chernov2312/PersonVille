function handleTestClose(closeUrl) {
    const confirmed = confirm(
        "Вы уверены, что хотите прервать тест?\n\nПрогресс текущего теста будет сброшен"
    );

    if (!confirmed) {
        return false;
    }

    fetch(closeUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
        .then((response) => {
            if (response.redirected) {
                window.location.href = response.url;
                return;
            }

            if (response.ok) {
                window.location.href = '/';
                return;
            }

            window.location.href = '/';
        })
        .catch((error) => {
            console.error('Error:', error);
            window.location.href = '/';
        });

    return false;
}

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i += 1) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === `${name}=`) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1),
                );
                break;
            }
        }
    }

    return cookieValue;
}
