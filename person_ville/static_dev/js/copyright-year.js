(function() {
    'use strict';
    document.addEventListener('DOMContentLoaded', function() {
        const yearElement = document.querySelector('.copyright-year');
        if (!yearElement) return;
        const serverYear = parseInt(yearElement.dataset.serverYear, 10);
        const now = new Date();
        const clientYear = now.getFullYear();
        const serverNewYear = new Date(Date.UTC(serverYear, 0, 1, 0, 0, 0));
        const diffHours = Math.abs(now - serverNewYear) / (1000 * 60 * 60);
        
        let displayYear;
        if (diffHours < 24) {
            displayYear = clientYear;
        } else {
            displayYear = serverYear;
        }
        
        yearElement.textContent = displayYear;
    });
})();