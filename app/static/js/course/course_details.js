/*
==========================================================
SkillForge LMS
Course Details
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    loadCourse();

});


/* ==========================================================
   Load Course
========================================================== */

async function loadCourse() {

    try {

        const response = await fetch(
            `/api/courses/${window.courseId}`
        );

        if (!response.ok) {

            throw new Error("Course not found.");

        }

        const course = await response.json();

        renderCourse(course);

    }

    catch (error) {

        console.error(error);

        document.getElementById("courseLoading").innerHTML = `

            <div class="alert alert-danger">

                Unable to load course details.

            </div>

        `;

    }

}


/* ==========================================================
   Render Course
========================================================== */

function renderCourse(course) {

    document.getElementById("courseLoading").style.display = "none";

    document.getElementById("courseContainer").style.display = "block";

    document.getElementById("courseTitle").textContent =
        course.title;

    document.getElementById("courseCategory").textContent =
        course.category;

    document.getElementById("courseDescription").textContent =
        course.description;

    document.getElementById("courseAbout").textContent =
        course.description;

    document.getElementById("courseLevel").textContent =
        course.level;

    document.getElementById("courseDuration").textContent =
        course.duration;

    document.getElementById("coursePrice").textContent =
        course.price;

    const status = document.getElementById("courseStatus");

    status.textContent =
        course.is_active ? "Active" : "Inactive";

    status.className =
        course.is_active
            ? "badge bg-success"
            : "badge bg-danger";

    document
        .getElementById("continueBtn")
        .addEventListener("click", () => {

            continueLearning(course.id);

        });

}


/* ==========================================================
   Continue Learning
========================================================== */

function continueLearning(courseId) {

    // Sprint 9
    // Redirect to Lesson Player

    window.location.href = `/learn/${courseId}`;

}