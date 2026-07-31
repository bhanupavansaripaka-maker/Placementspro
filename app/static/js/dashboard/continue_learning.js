/*
==========================================================
SkillForge LMS
Continue Learning
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    loadContinueLearning();

});

async function loadContinueLearning() {

    const container = document.getElementById(
        "continueLearningContainer"
    );

    if (!container) {
        return;
    }

    try {

        const course = await DashboardAPI.getContinueLearning();

        // No enrolled courses
        if (!course) {

            container.innerHTML = `
                <div class="text-center">

                    <p class="text-muted mb-3">

                        You haven't enrolled in any courses yet.

                    </p>

                    <a
                        href="/courses"
                        class="btn btn-primary btn-sm">

                        Browse Courses

                    </a>

                </div>
            `;

            return;

        }

        container.innerHTML = `

            <span class="badge bg-primary mb-2">

                ${course.category}

            </span>

            <h6 class="fw-bold">

                ${course.title}

            </h6>

            <p class="mb-1">

                <strong>Level:</strong>

                ${course.level}

            </p>

            <p class="mb-3">

                <strong>Duration:</strong>

                ${course.duration} Hours

            </p>

            <button
                class="btn btn-success w-100"
                onclick="continueLearning(${course.course_id})">

                Continue Learning

            </button>

        `;

    }

    catch (error) {

        console.error("Continue Learning Error:", error);

        container.innerHTML = `

            <div class="alert alert-danger mb-0">

                Failed to load course.

            </div>

        `;

    }

}

function continueLearning(courseId) {

    // TODO:
    // Redirect to the course learning page in Sprint 7.

    window.location.href = `/courses/${courseId}`;

}