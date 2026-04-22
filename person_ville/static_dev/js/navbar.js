function confirmLogout(hasCityResult) {
    if (hasCityResult) {
        return confirm(
            "Вы уверены, что хотите выйти?\n\nТекущий город будет сброшен"
        );
    }

    return confirm("Вы уверены, что хотите выйти из аккаунта?");
}

document.addEventListener("DOMContentLoaded", function () {
    const toggler = document.getElementById("navbarToggler");
    const closeBtn = document.getElementById("navbarClose");
    const overlay = document.getElementById("navbarOverlay");
    const navbarMenu = document.getElementById("navbarNav");

    function openMenu() {
        if (!navbarMenu) {
            return;
        }

        navbarMenu.style.display = "block";
        navbarMenu.classList.add("is-open");

        if (overlay) {
            overlay.style.display = "block";
            overlay.classList.add("is-open");
        }

        document.body.style.overflow = "hidden";
    }

    function closeMenu() {
        if (!navbarMenu) {
            return;
        }

        navbarMenu.style.display = "";
        navbarMenu.classList.remove("is-open");

        if (overlay) {
            overlay.style.display = "";
            overlay.classList.remove("is-open");
        }

        document.body.style.overflow = "";
    }

    if (toggler && navbarMenu) {
        toggler.addEventListener("click", function (event) {
            event.preventDefault();
            openMenu();
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", function (event) {
            event.preventDefault();
            closeMenu();
        });
    }

    if (overlay) {
        overlay.addEventListener("click", function (event) {
            event.preventDefault();
            closeMenu();
        });
    }

    const dropdown = document.getElementById("profileDropdown");
    const trigger = document.getElementById("profileDropdownTrigger");
    const dropdownMenu = document.getElementById("profileDropdownMenu");

    function openDropdown() {
        if (!dropdown || !trigger) {
            return;
        }

        dropdown.classList.add("is-open");
        trigger.setAttribute("aria-expanded", "true");
    }

    function closeDropdown() {
        if (!dropdown || !trigger) {
            return;
        }

        dropdown.classList.remove("is-open");
        trigger.setAttribute("aria-expanded", "false");
    }

    function toggleDropdown() {
        if (!dropdown) {
            return;
        }

        if (dropdown.classList.contains("is-open")) {
            closeDropdown();
        } else {
            openDropdown();
        }
    }

    if (dropdown && trigger && dropdownMenu) {
        trigger.addEventListener("click", function (event) {
            event.preventDefault();
            event.stopPropagation();
            toggleDropdown();
        });

        document.addEventListener("click", function (event) {
            if (!dropdown.contains(event.target)) {
                closeDropdown();
            }
        });
    }

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeDropdown();
            closeMenu();
        }
    });
});
