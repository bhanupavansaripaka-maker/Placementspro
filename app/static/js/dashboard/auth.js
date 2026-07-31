/*
==========================================================
SkillForge LMS
Dashboard Authentication Helper
==========================================================
*/

async function getCurrentStudent() {

    const token = localStorage.getItem("access_token");

    // User not logged in
    if (!token) {

        window.location.href = "/login";
        return null;
    }

    try {

        const response = await fetch("/students/profile", {

            method: "GET",

            headers: {
                "Authorization": `Bearer ${token}`
            }

        });

        if (response.status === 401) {

            localStorage.removeItem("access_token");
            localStorage.removeItem("token_type");

            window.location.href = "/login";
            return null;
        }

        if (!response.ok) {

            throw new Error("Unable to load student profile.");
        }

        const student = await response.json();

        return student;

    }
    catch (error) {

        console.error(error);
        return null;
    }
}