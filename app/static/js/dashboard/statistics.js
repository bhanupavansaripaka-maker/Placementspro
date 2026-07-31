/*
==========================================================
SkillForge LMS
Dashboard Statistics
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    loadDashboardStatistics();

});

async function loadDashboardStatistics() {

    try {

        const statistics = await DashboardAPI.getStatistics();

        document.getElementById("totalCourses").textContent =
            statistics.total_courses;

        document.getElementById("completedCourses").textContent =
            statistics.completed_courses;

        document.getElementById("activeCourses").textContent =
            statistics.active_courses;

        document.getElementById("certificatesEarned").textContent =
            statistics.certificates_earned;

    }

    catch (error) {

        console.error("Statistics Error:", error);

    }

}