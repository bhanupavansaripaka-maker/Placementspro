/*
==========================================================
SkillForge LMS
Course Details
==========================================================
*/

document.addEventListener("DOMContentLoaded", async () => {

    try {

        const courseId = window.location.pathname.split("/").pop();

        const response = await fetch(`/api/courses/${courseId}`);

        if (!response.ok) {

            throw new Error("Unable to load course.");

        }

        const course = await response.json();

        document.getElementById("courseTitle").textContent =
            course.title;

        document.getElementById("courseCategory").textContent =
            `${course.category} • ${course.level}`;

        document.getElementById("courseDescription").textContent =
            course.description;

        document.getElementById("courseCategory2").textContent =
            course.category;

        document.getElementById("courseLevel").textContent =
            course.level;

        document.getElementById("courseDuration").textContent =
            `${course.duration} Hours`;

        document.getElementById("coursePrice").textContent =
            course.price;

    }

    catch (error) {

        console.error(error);

        document.getElementById("courseTitle").textContent =
            "Course Not Found";

        document.getElementById("courseDescription").textContent =
            "Unable to load the requested course.";

    }

});