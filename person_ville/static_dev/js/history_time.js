function formatLocalDateTime(dateObj) {
    const day = String(dateObj.getDate()).padStart(2, '0');
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const year = dateObj.getFullYear();

    const hours = String(dateObj.getHours()).padStart(2, '0');
    const minutes = String(dateObj.getMinutes()).padStart(2, '0');

    return `${day}.${month}.${year} ${hours}:${minutes}`;
}

document.addEventListener('DOMContentLoaded', function () {
    const dateNodes = document.querySelectorAll('.js-local-datetime');

    dateNodes.forEach((node) => {
        const rawValue = node.dataset.serverDatetime;
        if (!rawValue) {
            return;
        }

        const parsedDate = new Date(rawValue);
        if (isNaN(parsedDate.getTime())) {
            return;
        }

        node.textContent = formatLocalDateTime(parsedDate);
    });
});
