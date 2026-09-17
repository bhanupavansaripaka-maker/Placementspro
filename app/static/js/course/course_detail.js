/*
==========================================================
SkillForge LMS
Public Course Details
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    loadCourse();

});


/* ==========================================================
   Load Course
========================================================== */

async function loadCourse() {

    console.log("=================================");
    console.log("COURSE PAGE DEBUG");
    console.log("COURSE_ID:", COURSE_ID);
    console.log("=================================");

    try {

        const url = `/api/courses/${COURSE_ID}`;

        console.log("Calling API:", url);

        const response = await fetch(url);

        console.log(
            "API Status:",
            response.status
        );

        console.log(
            "API OK:",
            response.ok
        );


        const responseText =
            await response.text();

        console.log(
            "API Response:",
            responseText
        );


        if (!response.ok) {

            throw new Error(
                `API returned ${response.status}: ${responseText}`
            );

        }


        const course =
            JSON.parse(responseText);

        console.log(
            "COURSE OBJECT:",
            course
        );


        renderCourse(course);

    }

    catch (error) {

        console.error(
            "FULL COURSE ERROR:",
            error
        );

        console.error(
            "ERROR MESSAGE:",
            error.message
        );

        showCourseError(
            error.message
        );

    }

}

/* ==========================================================
   Render Course
========================================================== */

function renderCourse(course) {

    /* ------------------------------------------------------
       Hide Loading
    ------------------------------------------------------ */

    const loading =
        document.getElementById(
            "courseLoading"
        );

    if (loading) {

        loading.style.display =
            "none";

    }


    /* ------------------------------------------------------
       Show Course
    ------------------------------------------------------ */

    const container =
        document.getElementById(
            "courseContainer"
        );

    if (container) {

        container.style.display =
            "block";

    }


    /* ------------------------------------------------------
       Course Information
    ------------------------------------------------------ */

    setText(
        "courseTitle",
        course.title
    );

    setText(
        "courseCategory",
        course.category
    );

    setText(
        "courseDescription",
        course.description
    );

    setText(
        "courseAbout",
        course.description
    );

    setText(
        "courseLevel",
        course.level
    );

    setText(
        "courseDuration",
        course.duration
    );

    setText(
        "coursePrice",
        course.price
    );


    /* ------------------------------------------------------
       Price Card
    ------------------------------------------------------ */

    const priceCard =
        document.getElementById(
            "coursePriceCard"
        );

    if (priceCard) {

        const price =
            Number(course.price || 0);

        if (price === 0) {

            priceCard.textContent =
                "FREE";

        }
        else {

            priceCard.textContent =
                `₹${price.toLocaleString("en-IN")}`;

        }

    }


    /* ------------------------------------------------------
       Course Statistics
    ------------------------------------------------------ */

    const modules =
        Array.isArray(course.modules)
            ? course.modules
            : [];


    let lessonCount = 0;


    modules.forEach(
        module => {

            if (
                Array.isArray(module.lessons)
            ) {

                lessonCount +=
                    module.lessons.length;

            }

        }
    );


    setText(
        "moduleCount",
        modules.length
    );

    setText(
        "lessonCount",
        lessonCount
    );

    setText(
        "courseLevelInfo",
        course.level
    );

    setText(
        "courseDurationInfo",
        course.duration
    );


    /* ------------------------------------------------------
       Curriculum
    ------------------------------------------------------ */

    renderCurriculum(
        modules
    );


    /* ------------------------------------------------------
       Start Learning Button
    ------------------------------------------------------ */

    const startButton =
        document.getElementById(
            "startLearningBtn"
        );

    if (startButton) {

        startButton.onclick = () => {

            startLearning(
                course.id
            );

        };

    }


    /* ------------------------------------------------------
       Bottom Start Learning Button
    ------------------------------------------------------ */

    const bottomButton =
        document.getElementById(
            "bottomStartLearningBtn"
        );

    if (bottomButton) {

        bottomButton.onclick = () => {

            startLearning(
                course.id
            );

        };

    }

}


/* ==========================================================
   Render Curriculum
========================================================== */

function renderCurriculum(
    modules
) {

    const curriculum =
        document.getElementById(
            "courseCurriculum"
        );


    if (!curriculum) {

        return;

    }


    /* ------------------------------------------------------
       No Modules
    ------------------------------------------------------ */

    if (
        !modules ||
        modules.length === 0
    ) {

        curriculum.innerHTML = `

            <div class="alert alert-info">

                Course curriculum will be
                available soon.

            </div>

        `;

        return;

    }


    /* ------------------------------------------------------
       Build Modules
    ------------------------------------------------------ */

    curriculum.innerHTML =
        modules
            .map(
                (module, index) => {

                    const lessons =
                        Array.isArray(
                            module.lessons
                        )
                            ? module.lessons
                            : [];


                    return `

                        <div
                            class="accordion-item mb-2">

                            <h2
                                class="accordion-header"
                                id="heading-${module.id}">

                                <button
                                    class="accordion-button ${
                                        index === 0
                                            ? ""
                                            : "collapsed"
                                    }"
                                    type="button"
                                    data-bs-toggle="collapse"
                                    data-bs-target="#module-${module.id}"
                                    aria-expanded="${
                                        index === 0
                                            ? "true"
                                            : "false"
                                    }">

                                    <strong>
                                        Module ${index + 1}:
                                    </strong>

                                    <span class="ms-2">
                                        ${escapeHtml(
                                            module.title
                                        )}
                                    </span>

                                </button>

                            </h2>


                            <div
                                id="module-${module.id}"
                                class="accordion-collapse collapse ${
                                    index === 0
                                        ? "show"
                                        : ""
                                }"
                                data-bs-parent="#courseCurriculum">

                                <div
                                    class="accordion-body">

                                    ${
                                        module.description
                                            ? `
                                                <p class="text-muted">
                                                    ${escapeHtml(
                                                        module.description
                                                    )}
                                                </p>
                                              `
                                            : ""
                                    }


                                    ${
                                        lessons.length === 0

                                            ? `

                                                <div class="text-muted">

                                                    No lessons available.

                                                </div>

                                              `

                                            : `

                                                <div class="list-group">

                                                    ${lessons
                                                        .map(
                                                            (
                                                                lesson,
                                                                lessonIndex
                                                            ) => `

                                                                <div
                                                                    class="list-group-item">

                                                                    <div
                                                                        class="d-flex justify-content-between align-items-center">

                                                                        <div>

                                                                            <strong>

                                                                                ${
                                                                                    lessonIndex + 1
                                                                                }.

                                                                                ${escapeHtml(
                                                                                    lesson.title
                                                                                )}

                                                                            </strong>


                                                                            ${
                                                                                lesson.topic
                                                                                    ? `

                                                                                        <div
                                                                                            class="small text-muted mt-1">

                                                                                            ${escapeHtml(
                                                                                                lesson.topic
                                                                                            )}

                                                                                        </div>

                                                                                      `
                                                                                    : ""
                                                                            }

                                                                        </div>


                                                                        ${
                                                                            lesson.estimated_minutes
                                                                                ? `

                                                                                    <span
                                                                                        class="badge bg-light text-dark">

                                                                                        ${lesson.estimated_minutes}
                                                                                        min

                                                                                    </span>

                                                                                  `
                                                                                : ""
                                                                        }

                                                                    </div>

                                                                </div>

                                                            `
                                                        )
                                                        .join("")}

                                                </div>

                                              `
                                    }

                                </div>

                            </div>

                        </div>

                    `;

                }
            )
            .join("");

}


/* ==========================================================
   Start Learning
========================================================== */

function startLearning(
    courseId
) {

    if (!courseId) {

        console.error(
            "Course ID is missing."
        );

        return;

    }


    console.log(
        "Starting course:",
        courseId
    );


    window.location.href =
        `/learn/${courseId}`;

}


/* ==========================================================
   Show Error
========================================================== */

function showCourseError(
    message
) {

    const loading =
        document.getElementById(
            "courseLoading"
        );

    if (loading) {

        loading.style.display =
            "none";

    }


    const container =
        document.getElementById(
            "courseContainer"
        );

    if (container) {

        container.style.display =
            "none";

    }


    const errorElement =
        document.getElementById(
            "courseError"
        );

    if (errorElement) {

        errorElement.textContent =
            message ||
            "Unable to load course.";

        errorElement.style.display =
            "block";

    }

}


/* ==========================================================
   Set Text Helper
========================================================== */

function setText(
    elementId,
    value
) {

    const element =
        document.getElementById(
            elementId
        );

    if (!element) {

        return;

    }


    element.textContent =
        value ?? "";

}


/* ==========================================================
   Escape HTML
========================================================== */

function escapeHtml(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";

    }


    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );

}