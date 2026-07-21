/*
==========================================================
SkillForge LMS
Dashboard
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    loadCurrentUser();

    initializeLogout();

});


/*
==========================================================
Load Logged In User
==========================================================
*/

async function loadCurrentUser() {

    const token = localStorage.getItem("access_token");

    if (!token) {

        window.location.href = "/login";

        return;

    }

    try {

        const response = await fetch("/auth/me", {

            headers: {

                Authorization: `Bearer ${token}`

            }

        });

        if (!response.ok) {

            throw new Error("Unauthorized");

        }

        const user = await response.json();

        document.getElementById("heroUserName").textContent =
            user.full_name;

        document.getElementById("navbarUserName").textContent =
            user.full_name;

    }

    catch (error) {

        console.error(error);

        localStorage.removeItem("access_token");

        window.location.href = "/login";

    }

}


/*
==========================================================
Logout
==========================================================
*/

function initializeLogout() {

    const logoutBtn = document.getElementById("logoutBtn");

    if (!logoutBtn) return;

    logoutBtn.addEventListener("click", (event) => {

        event.preventDefault();

        localStorage.removeItem("access_token");

        window.location.href = "/login";

    });

}