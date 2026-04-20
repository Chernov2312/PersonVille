(function() {
    'use strict';
    document.addEventListener('DOMContentLoaded', function() {

        const yearElement = document.querySelector('.copyright-year');
        if (!yearElement) {
            console.log('Year element not found');
            return;
        }

        const serverYear = parseInt(yearElement.dataset.serverYear, 10);
        const clientDate = new Date();
        const clientYear = clientDate.getFullYear();
        const serverDate = new Date(serverYear, 0, 1);
        const timeDiff = Math.abs(clientDate - serverDate);
        const hoursDiff = timeDiff / (1000 * 60 * 60);
        let displayYear;
        if (hoursDiff > 24) {
            displayYear = serverYear;
        } else {
            displayYear = clientYear;
        }


        console.log('Final display year:', displayYear);
    });
})();