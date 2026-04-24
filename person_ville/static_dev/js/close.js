function handleTestClose(closeUrl) {
    if (confirm("Вы уверены, что хотите прервать тест")) {
        fetch(closeUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        }).then(response => {
            window.location.href = '/';
        }).catch(() => {
            window.location.href = '/';
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