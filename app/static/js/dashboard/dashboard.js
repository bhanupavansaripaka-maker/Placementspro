/*
==========================================================
SkillForge LMS
Dashboard
==========================================================
*/

document.addEventListener("DOMContentLoaded", async () => {

    // If the dashboard hero is not present,
    // this is not the dashboard page.
    if (!document.getElementById("heroUserName")) {
        return;
    }

    await initializeDashboard();

});

async function initializeDashboard() {

    const student = await getCurrentStudent();

    if (!student) {
        return;
    }

    window.currentStudent = student;

    loadCurrentUser(student);

}

function loadCurrentUser(student) {

    updateHero(student);

    updateNavbar(student);

}

function updateHero(student) {

    const heroUserName = document.getElementById("heroUserName");

    if (heroUserName) {

        heroUserName.textContent = student.full_name;

    }

}

function updateNavbar(student) {

    const navbarUserName = document.getElementById("navbarUserName");

    if (navbarUserName) {

        navbarUserName.textContent = student.full_name;

    }

}