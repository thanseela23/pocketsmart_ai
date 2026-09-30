async function api(url, options = {}) {
    const config = {
        credentials: "include",
        ...options,
        headers: {
            ...(options.headers || {})
        }
    };

    if (
        options.body &&
        !(options.body instanceof FormData)
    ) {
        config.headers["Content-Type"] =
            "application/json";

        config.body = JSON.stringify(
            options.body
        );
    }

    const response = await fetch(
        url,
        config
    );

    let data = {};

    try {
        data = await response.json();
    } catch (_) {
        data = {};
    }

    return {
        ok: response.ok,
        status: response.status,
        data
    };
}


function escapeHtml(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        function (character) {

            const entities = {
                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                '"': "&quot;",
                "'": "&#039;"
            };

            return entities[
                character
            ];
        }
    );
}


async function updateNavigation() {

    const authLink =
        document.getElementById(
            "auth-link"
        );

    const logoutButton =
        document.getElementById(
            "logout-btn"
        );

    if (
        !authLink ||
        !logoutButton
    ) {
        return;
    }

    const result = await api(
        "/api/auth/session-info"
    );

    if (result.ok) {

        authLink.textContent =
            "Dashboard";

        authLink.href =
            "/dashboard";

        logoutButton.classList.remove(
            "hidden"
        );

        logoutButton.addEventListener(
            "click",
            async function () {

                await api(
                    "/api/auth/logout",
                    {
                        method: "POST"
                    }
                );

                window.location.href =
                    "/";
            }
        );
    }
}


updateNavigation();