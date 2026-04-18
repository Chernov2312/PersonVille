function formatClientDate(dateObj) {
    const day = String(dateObj.getDate()).padStart(2, '0');
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const year = dateObj.getFullYear();
    return `${day}.${month}.${year}`;
}

(function applyClientDateIfAvailable() {
    const dateNode = document.getElementById('characterDate');
    if (!dateNode) return;

    try {
        const clientDate = new Date();
        if (!isNaN(clientDate.getTime())) {
            dateNode.textContent = formatClientDate(clientDate);
        }
    } catch (error) {
        dateNode.textContent = dateNode.dataset.serverDate || '';
    }
})();

async function downloadCharacterCard() {
    const toolbar = document.getElementById('characterToolbar');
    const card = document.getElementById('characterCardExport');

    if (!card || !window.html2canvas) {
        alert('Не удалось подготовить карточку к скачиванию.');
        return;
    }

    toolbar.classList.add('is-hidden');

    await new Promise(resolve => requestAnimationFrame(resolve));

    try {
        const rect = card.getBoundingClientRect();

        const canvas = await html2canvas(card, {
            backgroundColor: null,
            scale: 2,
            useCORS: true,
            logging: false,
            x: 0,
            y: 0,
            width: Math.ceil(rect.width),
            height: Math.ceil(rect.height),
            scrollX: 0,
            scrollY: 0,
            windowWidth: Math.ceil(rect.width),
            windowHeight: Math.ceil(rect.height)
        });

        const link = document.createElement('a');
        link.download = 'personville_result.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    } catch (error) {
        console.error('Download error:', error);
        alert('Не удалось скачать карточку.');
    } finally {
        toolbar.classList.remove('is-hidden');
    }
}