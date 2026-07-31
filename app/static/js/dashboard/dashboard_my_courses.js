/*
==========================================================
SkillForge LMS
Dashboard - My Courses Widget
==========================================================
*/

document.addEventListener("DOMContentLoaded", async () => {

    const container = document.getElementById("myCoursesContainer");

    // Exit if the widget is not on the page
    if (!container) {
        return;
    }

    try {

        const courses = await DashboardAPI.getMyCourses();

        renderDashboardCourses(container, courses);

    } catch (error) {

        console.error("Failed to load dashboard courses:", error);

        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger">
                    Unable to load your courses.
                </div>
            </div>
        `;

    }

});

function renderDashboardCourses(container, courses) {

    container.innerHTML = "";

    if (!Array.isArray(courses) || courses.length === 0) {

        container.innerHTML = `
            <div class="col-12">

                <div class="alert alert-info mb-0">

                    <h6 class="mb-2">
                        No Courses Found
                    </h6>

                    <p class="mb-3">
                        You haven't enrolled in any courses yet.
                    </p>

                    <a
                        href="/courses"
                        class="btn btn-primary btn-sm">

                        Browse Courses

                    </a>

                </div>

            </div>
        `;

        return;

    }

    // Show only the latest 3 courses on the dashboard
    const recentCourses = courses.slice(0, 3);

    recentCourses.forEach(course => {

        container.innerHTML += `
            <div class="col-lg-4">

                <div class="card shadow-sm border-0 h-100">

                    <div class="card-body d-flex flex-column">

                        <span class="badge bg-primary mb-2">

                            ${course.category}

                        </span>

                        <h5 class="card-title">

                            ${course.title}

                        </h5>

                        <p class="text-muted mb-2">

                            ${course.level}

                        </p>

                        <p class="mb-3">

                            <strong>${course.duration}</strong> Hours

                        </p>

                        <div class="mt-auto">

                            <a
                                href="/courses/${course.course_id}"
                                class="btn btn-outline-primary w-100">

                                Continue Learning

                            </a>

                        </div>

                    </div>

                </div>

            </div>
        `;

    });

}