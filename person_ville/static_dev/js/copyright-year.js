(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        const yearElement = document.querySelector('.copyright-year');
        if (!yearElement) return;

        const rawServerYear = yearElement.dataset.serverYear;
        const serverYear = parseInt(rawServerYear, 10);

        if (Number.isNaN(serverYear)) {
            yearElement.textContent = new Date().getFullYear();
            return;
        }

        yearElement.textContent = serverYear;
    });
})();
