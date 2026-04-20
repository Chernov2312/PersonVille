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

function cropTransparentCanvas(sourceCanvas, padding = 16) {
    const ctx = sourceCanvas.getContext('2d');
    const { width, height } = sourceCanvas;
    const imageData = ctx.getImageData(0, 0, width, height).data;

    let top = height;
    let left = width;
    let right = 0;
    let bottom = 0;
    let found = false;

    for (let y = 0; y < height; y += 1) {
        for (let x = 0; x < width; x += 1) {
            const alpha = imageData[(y * width + x) * 4 + 3];
            if (alpha > 0) {
                found = true;
                if (x < left) left = x;
                if (x > right) right = x;
                if (y < top) top = y;
                if (y > bottom) bottom = y;
            }
        }
    }

    if (!found) {
        return sourceCanvas;
    }

    left = Math.max(0, left - padding);
    top = Math.max(0, top - padding);
    right = Math.min(width - 1, right + padding);
    bottom = Math.min(height - 1, bottom + padding);

    const croppedWidth = right - left + 1;
    const croppedHeight = bottom - top + 1;

    const croppedCanvas = document.createElement('canvas');
    croppedCanvas.width = croppedWidth;
    croppedCanvas.height = croppedHeight;

    const croppedCtx = croppedCanvas.getContext('2d');
    croppedCtx.drawImage(
        sourceCanvas,
        left,
        top,
        croppedWidth,
        croppedHeight,
        0,
        0,
        croppedWidth,
        croppedHeight
    );

    return croppedCanvas;
}

async function downloadCharacterCard() {
    const toolbar = document.getElementById('characterToolbar');
    const card = document.getElementById('characterCardExport');

    if (!card || !window.html2canvas) {
        alert('Не удалось подготовить карточку к скачиванию.');
        return;
    }

    toolbar.classList.add('is-hidden');
    await new Promise(resolve => setTimeout(resolve, 250));

    const exportBox = document.createElement('div');
    exportBox.style.position = 'fixed';
    exportBox.style.left = '-100000px';
    exportBox.style.top = '0';
    exportBox.style.width = '1700px';
    exportBox.style.height = '1500px';
    exportBox.style.paddingTop = '260px';
    exportBox.style.paddingLeft = '60px';
    exportBox.style.paddingRight = '60px';
    exportBox.style.paddingBottom = '60px';
    exportBox.style.background = 'transparent';
    exportBox.style.overflow = 'visible';
    exportBox.style.boxSizing = 'border-box';

    const clone = card.cloneNode(true);
    clone.style.width = '1500px';
    clone.style.minHeight = '1320px';
    clone.style.height = '1320px';
    clone.style.margin = '0 auto';
    clone.style.position = 'relative';

    exportBox.appendChild(clone);
    document.body.appendChild(exportBox);

    try {
        const canvas = await html2canvas(exportBox, {
            backgroundColor: null,
            scale: 2,
            useCORS: true,
            logging: false,
            scrollX: 0,
            scrollY: 0,
            windowWidth: 1700,
            windowHeight: 1500
        });

        const croppedCanvas = cropTransparentCanvas(canvas, 12);

        const link = document.createElement('a');
        link.download = 'personville_result.png';
        link.href = croppedCanvas.toDataURL('image/png');
        link.click();
    } catch (error) {
        console.error('Download error:', error);
        alert('Не удалось скачать карточку.');
    } finally {
        document.body.removeChild(exportBox);
        toolbar.classList.remove('is-hidden');
    }
}
