const circle = document.createElement('div');
circle.className = 'cursor-circle';
document.body.appendChild(circle);

let mouseX = window.innerWidth / 2;
let mouseY = window.innerHeight / 2;
let currentX = mouseX;
let currentY = mouseY;
let visible = false;
let rafId = null;

function showCursor() {
    if (!visible) {
        visible = true;
        circle.classList.add('is-visible');
    }
}

function hideCursor() {
    visible = false;
    circle.classList.remove('is-visible', 'is-hover');
}

function animateCursor() {
    currentX += (mouseX - currentX) * 0.18;
    currentY += (mouseY - currentY) * 0.18;

    circle.style.left = `${currentX}px`;
    circle.style.top = `${currentY}px`;

    rafId = requestAnimationFrame(animateCursor);
}

if (!rafId) {
    animateCursor();
}

document.addEventListener('pointermove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    showCursor();
});

document.addEventListener('pointerdown', () => {
    circle.classList.add('is-pressed');
});

document.addEventListener('pointerup', () => {
    circle.classList.remove('is-pressed');
});

document.addEventListener('mouseleave', hideCursor);
document.addEventListener('mouseout', (e) => {
    if (!e.relatedTarget) {
        hideCursor();
    }
});

window.addEventListener('blur', hideCursor);

document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        hideCursor();
    }
});

const hoverSelector = [
    'a',
    'button',
    'input',
    'textarea',
    'select',
    'label',
    '.custom-button',
    '.custom-inactive',
    '.homepage-test-button',
    '.city-street-link',
    '.city-character-button',
    '.city-finalize-button',
    '.character-toolbar-button',
    '.street-door-sign',
    '.question-save-button',
    '.btn-submit',
    '.auth-close',
    '.sent-close'
].join(',');

document.addEventListener('mouseover', (e) => {
    const target = e.target.closest(hoverSelector);
    if (target) {
        circle.classList.add('is-hover');
    }
});

document.addEventListener('mouseout', (e) => {
    const fromTarget = e.target.closest(hoverSelector);
    const toTarget = e.relatedTarget && e.relatedTarget.closest
        ? e.relatedTarget.closest(hoverSelector)
        : null;

    if (fromTarget && !toTarget) {
        circle.classList.remove('is-hover');
    }
});
