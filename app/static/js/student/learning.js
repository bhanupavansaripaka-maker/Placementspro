/*
==========================================================
SkillForge LMS
Student Learning Player
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    loadLearningCourse();

});


/* ==========================================================
   Load Course
========================================================== */

async function loadLearningCourse() {

    try {

        const response = await fetch(
            `/api/learning/course/${COURSE_ID}`
        );

        if (!response.ok) {

            throw new Error(
                `Unable to load course. Status: ${response.status}`
            );

        }

        const course = await response.json();

        renderCourse(course);

    }

    catch (error) {

        console.error(
            "Learning course error:",
            error
        );

        showError(
            "Unable to load the course. Please try again."
        );

    }

}


/* ==========================================================
   Render Course
========================================================== */

function renderCourse(course) {

    const courseTitle =
        document.getElementById("courseTitle");

    const courseDescription =
        document.getElementById("courseDescription");


    if (courseTitle) {

        courseTitle.textContent =
            course.title || "Course";

    }


    if (courseDescription) {

        courseDescription.textContent =
            course.description || "";

    }


    renderCurriculum(course);

}


/* ==========================================================
   Render Curriculum
========================================================== */

function renderCurriculum(course) {

    const container =
        document.getElementById(
            "curriculumContainer"
        );


    if (!container) {

        return;

    }


    container.innerHTML = "";


    const modules =
        course.modules || [];


    if (modules.length === 0) {

        container.innerHTML = `

            <div class="p-4 text-center text-muted">

                <i class="bi bi-journal-x fs-2"></i>

                <p class="mt-2 mb-0">

                    No lessons are available yet.

                </p>

            </div>

        `;

        return;

    }


    modules.forEach(
        (module, moduleIndex) => {

            const moduleHeader =
                document.createElement("div");


            moduleHeader.className =
                "p-3 bg-light border-bottom";


            moduleHeader.innerHTML = `

                <div class="fw-bold">

                    Module ${moduleIndex + 1}

                </div>

                <div class="small text-muted">

                    ${escapeHtml(
                        module.title || ""
                    )}

                </div>

            `;


            container.appendChild(
                moduleHeader
            );


            const lessons =
                module.lessons || [];


            if (lessons.length === 0) {

                const emptyLesson =
                    document.createElement("div");


                emptyLesson.className =
                    "p-3 text-muted small";


                emptyLesson.textContent =
                    "No lessons available.";


                container.appendChild(
                    emptyLesson
                );

                return;

            }


            lessons.forEach(
                (lesson, lessonIndex) => {

                    const lessonButton =
                        document.createElement("button");


                    lessonButton.type =
                        "button";


                    lessonButton.className =
                        "list-group-item list-group-item-action";


                    lessonButton.innerHTML = `

                        <div class="d-flex align-items-start">

                            <div class="me-3">

                                <span class="badge bg-primary">

                                    ${lessonIndex + 1}

                                </span>

                            </div>


                            <div>

                                <div class="fw-semibold">

                                    ${escapeHtml(
                                        lesson.title || ""
                                    )}

                                </div>


                                <div class="small text-muted">

                                    ${escapeHtml(
                                        lesson.topic || ""
                                    )}

                                </div>


                                <div class="small text-muted mt-1">

                                    <i class="bi bi-clock me-1"></i>

                                    ${lesson.estimated_minutes || 15}
                                    minutes

                                </div>

                            </div>

                        </div>

                    `;


                    lessonButton.addEventListener(
                        "click",
                        () => {

                            selectLesson(
                                lesson
                            );

                        }
                    );


                    container.appendChild(
                        lessonButton
                    );

                }
            );

        }
    );

}


/* ==========================================================
   Select Lesson
========================================================== */

function selectLesson(lesson) {

    const title =
        document.getElementById(
            "lessonTitle"
        );


    const content =
        document.getElementById(
            "lessonContent"
        );


    if (!title || !content) {

        return;

    }


    title.textContent =
        lesson.title || "Lesson";


    content.innerHTML = `

        <div class="mb-4">

            <span class="badge bg-primary">

                ${escapeHtml(
                    lesson.difficulty || "Beginner"
                )}

            </span>

        </div>


        <h5 class="fw-bold">

            ${escapeHtml(
                lesson.topic || ""
            )}

        </h5>


        <p class="text-muted">

            Ready to begin this lesson.

        </p>


        <button
            id="startLessonBtn"
            class="btn btn-primary mt-3">

            <i class="bi bi-play-fill me-2"></i>

            Start Lesson

        </button>

    `;


    document
        .getElementById("startLessonBtn")
        .addEventListener(
            "click",
            () => {

                loadLessonContent(
                    lesson.id
                );

            }
        );

}


/* ==========================================================
   Load AI Lesson Content
========================================================== */

async function loadLessonContent(lessonId) {

    const content =
        document.getElementById(
            "lessonContent"
        );


    if (!content) {

        return;

    }


    /* ------------------------------------------------------
       Loading State
    ------------------------------------------------------ */

    content.innerHTML = `

        <div class="text-center py-5">

            <div
                class="spinner-border text-primary"
                role="status">

            </div>


            <h5 class="mt-3">

                Generating your lesson...

            </h5>


            <p class="text-muted">

                Our AI is preparing personalized
                learning content for you.

            </p>

        </div>

    `;


    try {

        const response = await fetch(
            `/api/learning/lesson/${lessonId}`
        );


        if (!response.ok) {

            const errorData =
                await response.json();

            throw new Error(
                errorData.detail ||
                "Unable to load lesson."
            );

        }


        const lesson =
            await response.json();


        renderLessonContent(
            lesson
        );

    }

    catch (error) {

        console.error(
            "Lesson loading error:",
            error
        );


        content.innerHTML = `

            <div class="alert alert-danger">

                <h5>

                    Unable to load lesson

                </h5>


                <p class="mb-0">

                    ${escapeHtml(
                        error.message
                    )}

                </p>

            </div>

        `;

    }

}


/* ==========================================================
   Render AI Lesson Content
========================================================== */

function renderLessonContent(lesson) {

    const title =
        document.getElementById(
            "lessonTitle"
        );


    const content =
        document.getElementById(
            "lessonContent"
        );


    if (!content) {

        return;

    }


    if (title) {

        title.textContent =
            lesson.lesson_title || "Lesson";

    }


    content.innerHTML = `

        <!-- Difficulty -->

        <div class="mb-4">

            <span class="badge bg-primary me-2">

                ${escapeHtml(
                    lesson.difficulty || "Beginner"
                )}

            </span>


            <span class="text-muted small">

                <i class="bi bi-clock me-1"></i>

                ${lesson.estimated_minutes || 15}
                minutes

            </span>

        </div>


        <!-- Explanation -->

        <section class="mb-5">

            <h4 class="fw-bold mb-3">

                <i class="bi bi-book me-2"></i>

                Lesson Explanation

            </h4>


            <div class="lesson-text">

                ${formatText(
                    lesson.explanation
                )}

            </div>

        </section>


        <!-- Learning Objectives -->

        <section class="mb-5">

            <h4 class="fw-bold mb-3">

                <i class="bi bi-bullseye me-2"></i>

                Learning Objectives

            </h4>


            ${formatList(
                lesson.learning_objectives
            )}

        </section>


        <!-- Examples -->

        <section class="mb-5">

            <h4 class="fw-bold mb-3">

                <i class="bi bi-lightbulb me-2"></i>

                Examples

            </h4>


            ${formatList(
                lesson.examples
            )}

        </section>


        <!-- Code Examples -->

        <section class="mb-5">

            <h4 class="fw-bold mb-3">

                <i class="bi bi-code-slash me-2"></i>

                Code Examples

            </h4>


            <pre class="bg-dark text-light p-3 rounded">

                <code>${escapeHtml(
                    lesson.code_examples || ""
                )}</code>

            </pre>

        </section>


        <!-- Key Points -->

        <section class="mb-5">

            <h4 class="fw-bold mb-3">

                <i class="bi bi-key me-2"></i>

                Key Points

            </h4>


            ${formatList(
                lesson.key_points
            )}

        </section>


        <!-- Practical Exercise -->

        <section class="mb-5">

            <h4 class="fw-bold mb-3">

                <i class="bi bi-pencil-square me-2"></i>

                Practical Exercise

            </h4>


            <div class="alert alert-light border">

                ${formatText(
                    lesson.practical_exercise
                )}

            </div>

        </section>


        <!-- Take Quiz -->

        <section class="mt-5 pt-4 border-top">

            <div class="card border-primary">

                <div class="card-body text-center p-4">

                    <i class="bi bi-patch-question-fill
                              text-primary fs-1"></i>

                    <h4 class="fw-bold mt-3">

                        Ready to Test Your Knowledge?

                    </h4>


                    <p class="text-muted">

                        Complete this lesson quiz to
                        check your understanding.

                    </p>


                    <button
                        id="takeQuizBtn"
                        class="btn btn-primary btn-lg mt-2">

                        <i class="bi bi-play-circle me-2"></i>

                        Take Quiz

                    </button>

                </div>

            </div>

        </section>

    `;


    /* ======================================================
       Take Quiz Button
    ====================================================== */

    const takeQuizButton =
        document.getElementById(
            "takeQuizBtn"
        );


    if (takeQuizButton) {

        takeQuizButton.addEventListener(
            "click",
            () => {

                window.location.href =
                    `/quiz/${lesson.lesson_id}`;

            }
        );

    }

}


/* ==========================================================
   Format Text
========================================================== */

function formatText(value) {

    if (!value) {

        return "";

    }


    return escapeHtml(value)
        .replace(
            /\n/g,
            "<br>"
        );

}


/* ==========================================================
   Format List
========================================================== */

function formatList(value) {

    if (!value) {

        return `
            <p class="text-muted">
                No information available.
            </p>
        `;

    }


    const items =
        value
        .split("\n")
        .filter(
            item => item.trim() !== ""
        );


    if (items.length === 0) {

        return `
            <p class="text-muted">
                No information available.
            </p>
        `;

    }


    return `

        <ul class="mb-0">

            ${items.map(
                item => `

                    <li class="mb-2">

                        ${escapeHtml(
                            item
                        )}

                    </li>

                `
            ).join("")}

        </ul>

    `;

}


/* ==========================================================
   Show Error
========================================================== */

function showError(message) {

    const container =
        document.getElementById(
            "curriculumContainer"
        );


    if (!container) {

        return;

    }


    container.innerHTML = `

        <div class="alert alert-danger m-3">

            ${escapeHtml(message)}

        </div>

    `;

}


/* ==========================================================
   Escape HTML
========================================================== */

function escapeHtml(value) {

    const div =
        document.createElement("div");


    div.textContent =
        value ?? "";


    return div.innerHTML;

}