document.addEventListener("DOMContentLoaded", () => {
    console.log("PocketSmart AI loaded successfully.");

    // Get Started buttons
    document.querySelectorAll("[data-action='get-started']").forEach((button) => {
        button.addEventListener("click", () => {
            window.location.href = "/register";
        });
    });

    // Login buttons
    document.querySelectorAll("[data-action='login']").forEach((button) => {
        button.addEventListener("click", () => {
            window.location.href = "/login";
        });
    });

    // Planner buttons
    document.querySelectorAll("[data-planner]").forEach((button) => {
        button.addEventListener("click", () => {
            const planner = button.dataset.planner;

            if (planner) {
                window.location.href = `/planner/${planner}`;
            }
        });
    });

    // Mobile navigation
    const menuButton = document.querySelector("[data-menu-button]");
    const mobileMenu = document.querySelector("[data-mobile-menu]");

    if (menuButton && mobileMenu) {
        menuButton.addEventListener("click", () => {
            mobileMenu.classList.toggle("active");
        });
    }

    // Auto-hide alerts
    document.querySelectorAll(".alert").forEach((alert) => {
        setTimeout(() => {
            alert.style.opacity = "0";

            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 4000);
    });

    // Form loading state
    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", () => {
            const submitButton = form.querySelector(
                "button[type='submit']"
            );

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.dataset.originalText = submitButton.textContent;
                submitButton.textContent = "Please wait...";
            }
        });
    });
});