/*
==========================================================
SkillForge LMS
Navbar
==========================================================
*/

document.addEventListener("DOMContentLoaded", async () => {

    try {

        const student = await DashboardAPI.getCurrentStudent();

        const nameElement = document.getElementById("navbarUserName");
        const roleElement = document.getElementById("navbarUserRole");
        const avatarElement = document.getElementById("navbarAvatar");

        if (nameElement) {
            nameElement.textContent = student.full_name;
        }

        if (roleElement) {
            roleElement.textContent = "Student";
        }

        if (avatarElement) {

            const encodedName = encodeURIComponent(student.full_name);

            avatarElement.src =
                `https://ui-avatars.com/api/?name=${encodedName}&background=2563eb&color=ffffff`;

        }

    } catch (error) {

        console.error("Failed to load navbar.", error);

    }

});