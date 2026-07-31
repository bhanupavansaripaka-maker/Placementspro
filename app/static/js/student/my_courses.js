/*
==========================================================
SkillForge LMS
My Courses
==========================================================
*/

document.addEventListener("DOMContentLoaded", async () => {
    await initializeMyCourses();
});

async function initializeMyCourses() {

    const container = document.getElementById("myCoursesContainer");

    if (!container) {
        return;
    }

    try {

        const courses = await DashboardAPI.getMyCourses();

        renderCourses(container, courses);

    } catch (error) {

        console.error("Failed to load courses:", error);

        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger">
                    Unable to load your courses. Please try again later.
                </div>
            </div>
        `;
    }

}

function renderCourses(container, courses) {

    if (!Array.isArray(courses)) {
        courses = [];
    }

    if (courses.length === 0) {

        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-info">

                    <h5>No Courses Found</h5>

                    <p>You haven't enrolled in any courses yet.</p>

                    <a href="/courses"
                       class="btn btn-primary">

                        Browse Courses

                    </a>

                </div>
            </div>
        `;

        return;
    }

    let html = "";

    courses.forEach(course => {

        const enrolledDate = course.enrolled_at
            ? new Date(course.enrolled_at).toLocaleDateString()
            : "-";

        html += `
            <div class="col-lg-6 col-xl-4">

                <div class="card shadow-sm h-100">

                    <div class="card-body d-flex flex-column">

                        <span class="badge bg-primary mb-2">
                            ${course.category}
                        </span>

                        <h5 class="card-title">
                            ${course.title}
                        </h5>

                        <p class="mb-2">
                            <strong>Level:</strong> ${course.level}
                        </p>

                        <p class="mb-2">
                            <strong>Duration:</strong> ${course.duration} Hours
                        </p>

                        <p class="mb-2">
                            <strong>Price:</strong> ₹${course.price}
                        </p>

                        <p class="mb-3">
                            <strong>Enrolled:</strong> ${enrolledDate}
                        </p>

                        <div class="mt-auto">

                            <button
                                class="btn btn-primary w-100"
                                onclick="continueLearning(${course.course_id})">

                                Continue Learning

                            </button>

                        </div>

                    </div>

                </div>

            </div>
        `;

    });

    container.innerHTML = html;

}

function continueLearning(courseId) {

    window.location.href = `/courses/${courseId}`;

}