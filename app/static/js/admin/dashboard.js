/*
==========================================================
SkillForge LMS
Admin Dashboard
==========================================================
*/

document.addEventListener("DOMContentLoaded", loadDashboard);

async function loadDashboard() {

    try {

        const response = await fetch("/admin/api/dashboard");

        const data = await response.json();

        document.getElementById("studentCount").textContent =
            data.students;

        document.getElementById("courseCount").textContent =
            data.courses;

        document.getElementById("enrollmentCount").textContent =
            data.enrollments;

        document.getElementById("aiCount").textContent =
            data.ai_generated;

    }

    catch (error) {

        console.error(error);

    }

}