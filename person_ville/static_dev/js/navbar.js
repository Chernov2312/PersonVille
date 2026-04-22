// navbar.js - управление бургер-меню
document.addEventListener('DOMContentLoaded', function() {
    const toggler = document.getElementById('navbarToggler');
    const closeBtn = document.getElementById('navbarClose');
    const overlay = document.getElementById('navbarOverlay');
    const menu = document.getElementById('navbarNav');

    console.log('Elements found:', {
        toggler: !!toggler,
        closeBtn: !!closeBtn,
        overlay: !!overlay,
        menu: !!menu
    });

    if (!toggler || !menu) {
        console.error('Critical elements not found!');
        return;
    }

    function openMenu() {
        console.log('openMenu called');
        menu.style.display = 'block';
        menu.classList.add('is-open');
        if (overlay) {
            overlay.style.display = 'block';
            overlay.classList.add('is-open');
        }
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        console.log('closeMenu called');
        menu.style.display = '';
        menu.classList.remove('is-open');
        if (overlay) {
            overlay.style.display = '';
            overlay.classList.remove('is-open');
        }
        document.body.style.overflow = '';
    }

    toggler.addEventListener('click', function(e) {
        e.preventDefault();
        console.log('Toggler clicked');
        openMenu();
    });

    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Close button clicked');
            closeMenu();
        });
    }

    if (overlay) {
        overlay.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Overlay clicked');
            closeMenu();
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            console.log('Escape pressed');
            closeMenu();
        }
    });
});