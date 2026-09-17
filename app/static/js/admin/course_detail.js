/*
==========================================================
SkillForge LMS
Admin Course Details JavaScript
==========================================================
*/


// ==========================================================
// Page Initialization
// ==========================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadCourse();

        initializeEditCourse();

        initializeAddModule();

        initializeEditModule();

    }
);


// ==========================================================
// Load Course
// ==========================================================

async function loadCourse() {

    try {

        const response =
            await fetch(
                `/admin/api/course/${COURSE_ID}`
            );


        if (!response.ok) {

            const result =
                await response.json()
                    .catch(() => ({}));

            throw new Error(
                getErrorMessage(
                    result,
                    "Failed to load course."
                )
            );

        }


        const course =
            await response.json();


        renderCourse(course);

    }

    catch (error) {

        console.error(
            "Load course error:",
            error
        );


        const container =
            document.getElementById(
                "courseContainer"
            );


        if (container) {

            container.innerHTML = `

                <div class="alert alert-danger">

                    ${escapeHtml(
                        error.message ||
                        "Failed to load course."
                    )}

                </div>

            `;

        }

    }

}


// ==========================================================
// Render Course
// ==========================================================

function renderCourse(course) {

    window.currentCourse =
        course;


    let html = `

        <div class="course-header">

            <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">

                <div>

                    <h2>
                        ${escapeHtml(
                            course.title
                        )}
                    </h2>

                    <p class="text-muted">

                        ${escapeHtml(
                            course.description || ""
                        )}

                    </p>

                </div>


                <div class="d-flex gap-2 flex-wrap">

                    <button
                        type="button"
                        class="btn btn-outline-primary"
                        onclick="openEditCourseModal()">

                        <i class="bi bi-pencil"></i>

                        Edit Course

                    </button>


                    <button
                        type="button"
                        class="btn ${
                            course.is_active
                                ? "btn-outline-warning"
                                : "btn-success"
                        }"
                        onclick="toggleCourseStatus()">

                        <i class="bi ${
                            course.is_active
                                ? "bi-eye-slash"
                                : "bi-check-circle"
                        }"></i>

                        ${
                            course.is_active
                                ? "Unpublish Course"
                                : "Publish Course"
                        }

                    </button>

                </div>

            </div>


            <div class="course-meta mt-3">

                <span class="badge bg-primary">

                    ${escapeHtml(
                        course.level || ""
                    )}

                </span>


                <span class="badge bg-dark">

                    ${escapeHtml(
                        course.category || ""
                    )}

                </span>


                <span class="badge ${
                    course.is_active
                        ? "bg-success"
                        : "bg-warning text-dark"
                }">

                    ${
                        course.is_active
                            ? "Published"
                            : "Draft"
                    }

                </span>

            </div>

        </div>


        <div
            class="accordion"
            id="courseAccordion">

    `;


    // ======================================================
    // Modules
    // ======================================================

    if (
        course.modules &&
        course.modules.length > 0
    ) {

        course.modules.forEach(
            (module, index) => {

                html += `

                    <div class="accordion-item module-card">

                        <div class="accordion-header">

                            <div class="d-flex align-items-center">

                                <button
                                    type="button"
                                    class="accordion-button ${
                                        index
                                            ? "collapsed"
                                            : ""
                                    }"
                                    data-bs-toggle="collapse"
                                    data-bs-target="#module${module.id}"
                                    aria-controls="module${module.id}">

                                    ${escapeHtml(
                                        module.title
                                    )}

                                </button>


                                <button
                                    type="button"
                                    class="btn btn-sm btn-outline-primary ms-2"
                                    onclick="openEditModuleModal(${module.id})">

                                    <i class="bi bi-pencil"></i>

                                    Edit

                                </button>


                                <button
                                    type="button"
                                    class="btn btn-sm btn-outline-danger ms-2"
                                    onclick="deleteModule(${module.id}, '${escapeJs(module.title)}')">

                                    <i class="bi bi-trash"></i>

                                    Delete

                                </button>

                            </div>

                        </div>


                        <div
                            id="module${module.id}"
                            class="accordion-collapse collapse ${
                                index === 0
                                    ? "show"
                                    : ""
                            }">

                            <div class="accordion-body">

                `;


                // ==================================================
                // Module Description
                // ==================================================

                if (module.description) {

                    html += `

                        <p class="text-muted">

                            ${escapeHtml(
                                module.description
                            )}

                        </p>

                    `;

                }


                // ==================================================
                // Lessons
                // ==================================================

                if (
                    module.lessons &&
                    module.lessons.length > 0
                ) {

                    module.lessons.forEach(
                        lesson => {

                            html += `

                                <div
                                    class="lesson-item mb-3 p-3 border rounded"
                                    id="lesson-${lesson.id}">

                                    <div class="d-flex justify-content-between align-items-center">

                                        <div>

                                            <div class="fw-semibold">

                                                📘

                                                ${escapeHtml(
                                                    lesson.title
                                                )}

                                            </div>

                                            <div class="small text-muted mt-1">

                                                ${escapeHtml(
                                                    lesson.topic || ""
                                                )}

                                            </div>

                                        </div>


                                        <div class="d-flex align-items-center gap-2">

                                            <span class="badge bg-secondary">

                                                ${escapeHtml(
                                                    lesson.difficulty || ""
                                                )}

                                            </span>


                                            <span class="badge bg-light text-dark">

                                                ${lesson.estimated_minutes || 0}
                                                min

                                            </span>

                                        </div>

                                    </div>


                                    <div class="mt-3">

                            `;


                            // ======================================
                            // AI Content Available
                            // ======================================

                            if (
                                lesson.has_content
                            ) {

                                html += `

                                    <span class="badge bg-success me-2">

                                        ✓ AI Content Available

                                    </span>


                                    <button
                                        type="button"
                                        class="btn btn-sm btn-outline-primary me-2"
                                        onclick="viewLessonContent(${lesson.id})">

                                        👁 View Content

                                    </button>


                                    <button
                                        type="button"
                                        class="btn btn-sm btn-outline-secondary me-2"
                                        onclick="editLessonContent(${lesson.id})">

                                        ✏️ Edit Content

                                    </button>


                                    <button
                                        type="button"
                                        class="btn btn-sm btn-outline-warning"
                                        onclick="generateLessonContent(${lesson.id})">

                                        🔄 Regenerate

                                    </button>

                                `;

                            }

                            else {

                                html += `

                                    <button
                                        type="button"
                                        class="btn btn-sm btn-outline-success"
                                        onclick="generateLessonContent(${lesson.id})">

                                        ✨ Generate AI Content

                                    </button>

                                `;

                            }


                            // ======================================
                            // Quiz Section
                            // ======================================

                            html += `

                                <div class="mt-3 pt-3 border-top">

                                    ${
                                        lesson.has_quiz
                                            ? `

                                            <span class="badge bg-info text-dark me-2">

                                                📝 Quiz Available

                                            </span>


                                            <span class="badge bg-light text-dark me-2">

                                                ${
                                                    lesson.quiz
                                                        ? lesson.quiz.question_count
                                                        : 0
                                                }
                                                Questions

                                            </span>


                                            <button
                                                type="button"
                                                class="btn btn-sm btn-outline-primary me-2"
                                                onclick="viewLessonQuiz(${lesson.id})">

                                                👁 View Quiz

                                            </button>


                                            <button
                                                type="button"
                                                class="btn btn-sm btn-outline-secondary"
                                                onclick="editLessonQuiz(${lesson.id})">

                                                ✏️ Edit Quiz

                                            </button>

                                        `
                                            : `

                                            <button
                                                type="button"
                                                class="btn btn-sm btn-outline-info"
                                                onclick="generateLessonQuiz(${lesson.id})">

                                                📝 Generate Quiz

                                            </button>

                                        `
                                    }

                                </div>

                            `;


                            html += `

                                    </div>

                                </div>

                            `;

                        }
                    );

                }

                else {

                    html += `

                        <div class="text-muted">

                            No lessons added yet.

                        </div>

                    `;

                }


                html += `

                            </div>

                        </div>

                    </div>

                `;

            }
        );

    }

    else {

        html += `

            <div class="alert alert-info">

                No modules have been added to this course yet.

            </div>

        `;

    }


    html += `

        </div>

    `;


    const container =
        document.getElementById(
            "courseContainer"
        );


    if (container) {

        container.innerHTML =
            html;

    }

}


// ==========================================================
// Publish / Unpublish Course
// ==========================================================

async function toggleCourseStatus() {

    if (!window.currentCourse) {

        alert(
            "Course information is not available."
        );

        return;

    }


    const course =
        window.currentCourse;


    const action =
        course.is_active
            ? "unpublish"
            : "publish";


    const confirmationMessage =
        course.is_active

            ? "Are you sure you want to unpublish this course?"

            : "Are you sure you want to publish this course?";


    if (!confirm(confirmationMessage)) {

        return;

    }


    try {

        const response =
            await fetch(
                `/admin/api/course/${COURSE_ID}/status`,
                {

                    method: "PUT",

                    headers: {

                        "Content-Type":
                            "application/json"

                    }

                }
            );


        const result =
            await response.json()
                .catch(() => ({}));


        if (!response.ok) {

            throw new Error(
                getErrorMessage(
                    result,
                    "Failed to update course status."
                )
            );

        }


        alert(
            result.message ||
            "Course status updated successfully."
        );


        await loadCourse();

    }

    catch (error) {

        console.error(
            "Course status update error:",
            error
        );


        alert(
            error.message ||
            "Failed to update course status."
        );

    }

}


// ==========================================================
// Initialize Edit Course
// ==========================================================

function initializeEditCourse() {

    const saveButton =
        document.getElementById(
            "saveCourseBtn"
        );


    if (!saveButton) {

        return;

    }


    saveButton.addEventListener(
        "click",
        saveCourse
    );

}


// ==========================================================
// Open Edit Course Modal
// ==========================================================

function openEditCourseModal() {

    if (!window.currentCourse) {

        return;

    }


    const course =
        window.currentCourse;


    document.getElementById(
        "courseTitle"
    ).value =
        course.title || "";


    document.getElementById(
        "courseCategory"
    ).value =
        course.category || "";


    document.getElementById(
        "courseLevel"
    ).value =
        course.level || "Beginner";


    document.getElementById(
        "courseDuration"
    ).value =
        course.duration || 0;


    document.getElementById(
        "coursePrice"
    ).value =
        course.price || 0;


    document.getElementById(
        "courseDescription"
    ).value =
        course.description || "";


    const modalElement =
        document.getElementById(
            "editCourseModal"
        );


    const modal =
        bootstrap.Modal.getOrCreateInstance(
            modalElement
        );


    modal.show();

}


// ==========================================================
// Save Course
// ==========================================================

async function saveCourse() {

    const saveButton =
        document.getElementById(
            "saveCourseBtn"
        );


    const data = {

        title:
            document.getElementById(
                "courseTitle"
            ).value.trim(),

        description:
            document.getElementById(
                "courseDescription"
            ).value.trim(),

        category:
            document.getElementById(
                "courseCategory"
            ).value.trim(),

        level:
            document.getElementById(
                "courseLevel"
            ).value,

        duration:
            Number(
                document.getElementById(
                    "courseDuration"
                ).value
            ),

        price:
            Number(
                document.getElementById(
                    "coursePrice"
                ).value
            )

    };


    if (!data.title) {

        alert(
            "Course title is required."
        );

        return;

    }


    try {

        saveButton.disabled = true;

        saveButton.innerText =
            "Saving...";


        const response =
            await fetch(
                `/admin/api/course/${COURSE_ID}`,
                {

                    method: "PUT",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify(data)

                }
            );


        const result =
            await response.json()
                .catch(() => ({}));


        if (!response.ok) {

            throw new Error(
                getErrorMessage(
                    result,
                    "Failed to update course."
                )
            );

        }


        alert(
            "Course updated successfully."
        );


        const modalElement =
            document.getElementById(
                "editCourseModal"
            );


        const modal =
            bootstrap.Modal.getInstance(
                modalElement
            );


        if (modal) {

            modal.hide();

        }


        await loadCourse();

    }

    catch (error) {

        console.error(error);

        alert(
            error.message ||
            "Failed to update course."
        );

    }

    finally {

        saveButton.disabled = false;

        saveButton.innerText =
            "Save Changes";

    }

}


// ==========================================================
// Initialize Add Module
// ==========================================================

function initializeAddModule() {

    const addButton =
        document.getElementById(
            "addModuleBtn"
        );


    const saveButton =
        document.getElementById(
            "saveModuleBtn"
        );


    if (addButton) {

        addButton.addEventListener(
            "click",
            openAddModuleModal
        );

    }


    if (saveButton) {

        saveButton.addEventListener(
            "click",
            saveModule
        );

    }

}


// ==========================================================
// Open Add Module Modal
// ==========================================================

function openAddModuleModal() {

    document.getElementById(
        "moduleTitle"
    ).value = "";


    document.getElementById(
        "moduleDescription"
    ).value = "";


    const modalElement =
        document.getElementById(
            "addModuleModal"
        );


    const modal =
        bootstrap.Modal.getOrCreateInstance(
            modalElement
        );


    modal.show();

}


// ==========================================================
// Save Module
// ==========================================================

async function saveModule() {

    const saveButton =
        document.getElementById(
            "saveModuleBtn"
        );


    const title =
        document.getElementById(
            "moduleTitle"
        ).value.trim();


    const description =
        document.getElementById(
            "moduleDescription"
        ).value.trim();


    if (!title) {

        alert(
            "Module title is required."
        );

        return;

    }


    const data = {

        title: title,

        description:
            description || null

    };


    try {

        saveButton.disabled = true;

        saveButton.innerText =
            "Saving...";


        const response =
            await fetch(
                `/admin/api/course/${COURSE_ID}/modules`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify(data)

                }
            );


        const result =
            await response.json()
                .catch(() => ({}));


        if (!response.ok) {

            throw new Error(
                getErrorMessage(
                    result,
                    "Failed to create module."
                )
            );

        }


        alert(
            "Module created successfully."
        );


        const modalElement =
            document.getElementById(
                "addModuleModal"
            );


        const modal =
            bootstrap.Modal.getInstance(
                modalElement
            );


        if (modal) {

            modal.hide();

        }


        await loadCourse();

    }

    catch (error) {

        console.error(error);

        alert(
            error.message ||
            "Failed to create module."
        );

    }

    finally {

        saveButton.disabled = false;

        saveButton.innerText =
            "Save Module";

    }

}


// ==========================================================
// Initialize Edit Module
// ==========================================================

function initializeEditModule() {

    const saveButton =
        document.getElementById(
            "saveEditModuleBtn"
        );


    if (!saveButton) {

        return;

    }


    saveButton.addEventListener(
        "click",
        saveEditModule
    );

}


// ==========================================================
// Open Edit Module Modal
// ==========================================================

function openEditModuleModal(
    moduleId
) {

    if (!window.currentCourse) {

        return;

    }


    const module =
        window.currentCourse.modules.find(
            item =>
                item.id === moduleId
        );


    if (!module) {

        alert(
            "Module not found."
        );

        return;

    }


    window.currentModuleId =
        moduleId;


    document.getElementById(
        "editModuleTitle"
    ).value =
        module.title || "";


    document.getElementById(
        "editModuleDescription"
    ).value =
        module.description || "";


    const modalElement =
        document.getElementById(
            "editModuleModal"
        );


    const modal =
        bootstrap.Modal.getOrCreateInstance(
            modalElement
        );


    modal.show();

}


// ==========================================================
// Save Edited Module
// ==========================================================

async function saveEditModule() {

    const saveButton =
        document.getElementById(
            "saveEditModuleBtn"
        );


    const moduleId =
        window.currentModuleId;


    if (!moduleId) {

        alert(
            "Module ID is missing."
        );

        return;

    }


    const title =
        document.getElementById(
            "editModuleTitle"
        ).value.trim();


    const description =
        document.getElementById(
            "editModuleDescription"
        ).value.trim();


    if (!title) {

        alert(
            "Module title is required."
        );

        return;

    }


    const data = {

        title: title,

        description:
            description || null

    };


    try {

        saveButton.disabled = true;

        saveButton.innerText =
            "Saving...";


        const response =
            await fetch(
                `/admin/api/module/${moduleId}`,
                {

                    method: "PUT",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify(data)

                }
            );


        const result =
            await response.json()
                .catch(() => ({}));


        if (!response.ok) {

            throw new Error(
                getErrorMessage(
                    result,
                    "Failed to update module."
                )
            );

        }


        alert(
            "Module updated successfully."
        );


        const modalElement =
            document.getElementById(
                "editModuleModal"
            );


        const modal =
            bootstrap.Modal.getInstance(
                modalElement
            );


        if (modal) {

            modal.hide();

        }


        await loadCourse();

    }

    catch (error) {

        console.error(error);

        alert(
            error.message ||
            "Failed to update module."
        );

    }

    finally {

        saveButton.disabled = false;

        saveButton.innerText =
            "Save Changes";

    }

}


// ==========================================================
// Delete Module
// ==========================================================

async function deleteModule(
    moduleId,
    moduleTitle
) {

    const confirmed =
        confirm(
            `Are you sure you want to delete "${moduleTitle}"?`
        );


    if (!confirmed) {

        return;

    }


    try {

        const response =
            await fetch(
                `/admin/api/module/${moduleId}`,
                {

                    method: "DELETE"

                }
            );


        const result =
            await response.json()
                .catch(() => ({}));


        if (!response.ok) {

            throw new Error(
                getErrorMessage(
                    result,
                    "Failed to delete module."
                )
            );

        }


        alert(
            "Module deleted successfully."
        );


        await loadCourse();

    }

    catch (error) {

        console.error(error);

        alert(
            error.message ||
            "Failed to delete module."
        );

    }

}


// ==========================================================
// Generate AI Lesson Content
// ==========================================================

async function generateLessonContent(
    lessonId
) {

    const button =
        window.event
            ? window.event.currentTarget
            : null;


    const originalText =
        button
            ? button.innerHTML
            : "✨ Generate AI Content";


    try {

        if (button) {

            button.disabled = true;

            button.innerHTML =
                `<span class="spinner-border spinner-border-sm me-1"></span>
                 Generating...`;

        }


        const response =
            await fetch(
                `/admin/api/lesson/${lessonId}/generate-content`,
                {

                    method: "POST"

                }
            );


        const result =
            await response.json()
                .catch(() => ({}));


        if (!response.ok) {

            throw new Error(
                getErrorMessage(
                    result,
                    "Failed to generate lesson content."
                )
            );

        }


        if (!result.content) {

            throw new Error(
                "AI returned no lesson content."
            );

        }


        showLessonContentModal(
            result.content
        );


        await loadCourse();

    }

    catch (error) {

        console.error(
            "Lesson content generation error:",
            error
        );


        alert(
            error.message ||
            "Failed to generate lesson content."
        );

    }

    finally {

        if (button) {

            button.disabled = false;

            button.innerHTML =
                originalText;

        }

    }

}


// ==========================================================
// View Saved Lesson Content
// ==========================================================

function viewLessonContent(
    lessonId
) {

    const lesson =
        findLesson(
            lessonId
        );


    if (!lesson) {

        alert(
            "Lesson not found."
        );

        return;

    }


    if (!lesson.has_content) {

        alert(
            "AI content has not been generated yet."
        );

        return;

    }


    showLessonContentModal(
        lesson.content
    );

}


// ==========================================================
// Find Lesson
// ==========================================================

function findLesson(
    lessonId
) {

    if (!window.currentCourse) {

        return null;

    }


    for (
        const module of
        window.currentCourse.modules
    ) {

        const lesson =
            module.lessons.find(
                item =>
                    item.id === lessonId
            );


        if (lesson) {

            return lesson;

        }

    }


    return null;

}


// ==========================================================
// Edit Lesson Content
// ==========================================================

function editLessonContent(
    lessonId
) {

    const lesson =
        findLesson(
            lessonId
        );


    if (!lesson) {

        alert(
            "Lesson not found."
        );

        return;

    }


    if (!lesson.has_content) {

        alert(
            "Generate lesson content first."
        );

        return;

    }


    window.currentEditingLessonId =
        lessonId;


    showEditLessonContentModal(
        lesson.content
    );

}


// ==========================================================
// Show Edit Lesson Content Modal
// ==========================================================

function showEditLessonContentModal(
    content
) {

    let modalElement =
        document.getElementById(
            "editLessonContentModal"
        );


    if (!modalElement) {

        modalElement =
            document.createElement(
                "div"
            );


        modalElement.id =
            "editLessonContentModal";


        modalElement.className =
            "modal fade";


        modalElement.tabIndex =
            -1;


        modalElement.innerHTML = `

            <div class="modal-dialog modal-xl modal-dialog-scrollable">

                <div class="modal-content">

                    <div class="modal-header">

                        <h5 class="modal-title">

                            ✏️ Edit AI Lesson Content

                        </h5>


                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal">

                        </button>

                    </div>


                    <div class="modal-body">

                        <div class="mb-3">

                            <label class="form-label fw-semibold">

                                Explanation

                            </label>


                            <textarea
                                id="editLessonExplanation"
                                class="form-control"
                                rows="7">
                            </textarea>

                        </div>


                        <div class="mb-3">

                            <label class="form-label fw-semibold">

                                Learning Objectives

                            </label>


                            <textarea
                                id="editLessonObjectives"
                                class="form-control"
                                rows="6">
                            </textarea>


                            <div class="form-text">

                                Enter one objective per line.

                            </div>

                        </div>


                        <div class="mb-3">

                            <label class="form-label fw-semibold">

                                Examples

                            </label>


                            <textarea
                                id="editLessonExamples"
                                class="form-control"
                                rows="6">
                            </textarea>


                            <div class="form-text">

                                Enter one example per line.

                            </div>

                        </div>


                        <div class="mb-3">

                            <label class="form-label fw-semibold">

                                Code Examples

                            </label>


                            <textarea
                                id="editLessonCodeExamples"
                                class="form-control font-monospace"
                                rows="10">
                            </textarea>


                            <div class="form-text">

                                Separate multiple code examples with a blank line.

                            </div>

                        </div>


                        <div class="mb-3">

                            <label class="form-label fw-semibold">

                                Practical Exercise

                            </label>


                            <textarea
                                id="editLessonExercise"
                                class="form-control"
                                rows="6">
                            </textarea>

                        </div>


                        <div class="mb-3">

                            <label class="form-label fw-semibold">

                                Key Points

                            </label>


                            <textarea
                                id="editLessonKeyPoints"
                                class="form-control"
                                rows="6">
                            </textarea>


                            <div class="form-text">

                                Enter one key point per line.

                            </div>

                        </div>

                    </div>


                    <div class="modal-footer">

                        <button
                            type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal">

                            Cancel

                        </button>


                        <button
                            type="button"
                            class="btn btn-primary"
                            id="saveLessonContentBtn">

                            💾 Save Changes

                        </button>

                    </div>

                </div>

            </div>

        `;


        document.body.appendChild(
            modalElement
        );


        document.getElementById(
            "saveLessonContentBtn"
        ).addEventListener(
            "click",
            saveLessonContent
        );

    }


    document.getElementById(
        "editLessonExplanation"
    ).value =
        content.explanation || "";


    document.getElementById(
        "editLessonObjectives"
    ).value =
        arrayToText(
            content.learning_objectives
        );


    document.getElementById(
        "editLessonExamples"
    ).value =
        arrayToText(
            content.examples
        );


    document.getElementById(
        "editLessonCodeExamples"
    ).value =
        arrayToCodeText(
            content.code_examples
        );


    document.getElementById(
        "editLessonExercise"
    ).value =
        content.practical_exercise || "";


    document.getElementById(
        "editLessonKeyPoints"
    ).value =
        arrayToText(
            content.key_points
        );


    const modal =
        bootstrap.Modal.getOrCreateInstance(
            modalElement
        );


    modal.show();

}


// ==========================================================
// Save Edited Lesson Content
// ==========================================================

async function saveLessonContent() {

    const lessonId =
        window.currentEditingLessonId;


    if (!lessonId) {

        alert(
            "Lesson ID is missing."
        );

        return;

    }


    const saveButton =
        document.getElementById(
            "saveLessonContentBtn"
        );


    const data = {

        explanation:
            document.getElementById(
                "editLessonExplanation"
            ).value.trim(),


        learning_objectives:
            textToArray(
                document.getElementById(
                    "editLessonObjectives"
                ).value
            ),


        examples:
            textToArray(
                document.getElementById(
                    "editLessonExamples"
                ).value
            ),


        code_examples:
            codeTextToArray(
                document.getElementById(
                    "editLessonCodeExamples"
                ).value
            ),


        practical_exercise:
            document.getElementById(
                "editLessonExercise"
            ).value.trim(),


        key_points:
            textToArray(
                document.getElementById(
                    "editLessonKeyPoints"
                ).value
            )

    };


    if (!data.explanation) {

        alert(
            "Explanation is required."
        );

        return;

    }


    if (!data.learning_objectives.length) {

        alert(
            "Add at least one learning objective."
        );

        return;

    }


    if (!data.examples.length) {

        alert(
            "Add at least one example."
        );

        return;

    }


    if (!data.code_examples.length) {

        alert(
            "Add at least one code example."
        );

        return;

    }


    if (!data.practical_exercise) {

        alert(
            "Practical exercise is required."
        );

        return;

    }


    if (!data.key_points.length) {

        alert(
            "Add at least one key point."
        );

        return;

    }


    try {

        saveButton.disabled = true;

        saveButton.innerText =
            "Saving...";


        const response =
            await fetch(
                `/admin/api/lesson/${lessonId}/content`,
                {

                    method: "PUT",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify(data)

                }
            );


        const result =
            await response.json()
                .catch(() => ({}));


        if (!response.ok) {

            throw new Error(
                getErrorMessage(
                    result,
                    "Failed to update lesson content."
                )
            );

        }


        alert(
            "Lesson content updated successfully."
        );


        const modalElement =
            document.getElementById(
                "editLessonContentModal"
            );


        const modal =
            bootstrap.Modal.getInstance(
                modalElement
            );


        if (modal) {

            modal.hide();

        }


        await loadCourse();


        const updatedLesson =
            findLesson(
                lessonId
            );


        if (
            updatedLesson &&
            updatedLesson.content
        ) {

            showLessonContentModal(
                updatedLesson.content
            );

        }

    }

    catch (error) {

        console.error(
            "Update lesson content error:",
            error
        );


        alert(
            error.message ||
            "Failed to update lesson content."
        );

    }

    finally {

        saveButton.disabled = false;

        saveButton.innerText =
            "💾 Save Changes";

    }

}


// ==========================================================
// Generate AI Quiz
// ==========================================================

async function generateLessonQuiz(
    lessonId
) {

    const numberOfQuestions =
        10;


    const confirmed =
        confirm(
            `Generate a ${numberOfQuestions}-question quiz for this lesson?`
        );


    if (!confirmed) {

        return;

    }


    try {

        const response =
            await fetch(
                `/admin/api/lesson/${lessonId}/generate-quiz`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            number_of_questions:
                                numberOfQuestions

                        })

                }
            );


        const result =
            await response.json()
                .catch(() => ({}));


        if (!response.ok) {

            throw new Error(
                getErrorMessage(
                    result,
                    "Failed to generate quiz."
                )
            );

        }


        if (
            !result.quiz
        ) {

            throw new Error(
                "Quiz was not returned by the server."
            );

        }


        alert(
            result.message ||
            "Quiz generated successfully."
        );


        await loadCourse();


        showLessonQuizModal(
            result.quiz
        );

    }

    catch (error) {

        console.error(
            "Quiz generation error:",
            error
        );


        alert(
            error.message ||
            "Failed to generate quiz."
        );

    }

}


// ==========================================================
// View Saved Quiz
// ==========================================================

async function viewLessonQuiz(
    lessonId
) {

    try {

        const response =
            await fetch(
                `/admin/api/lesson/${lessonId}/quiz`
            );


        const result =
            await response.json()
                .catch(() => ({}));


        if (!response.ok) {

            throw new Error(
                getErrorMessage(
                    result,
                    "Quiz not found."
                )
            );

        }


        if (
            !result.quiz
        ) {

            throw new Error(
                "Quiz data is not available."
            );

        }


        showLessonQuizModal(
            result.quiz
        );

    }

    catch (error) {

        console.error(
            "View quiz error:",
            error
        );


        alert(
            error.message ||
            "Failed to load quiz."
        );

    }

}


// ==========================================================
// Edit Lesson Quiz
// ==========================================================

async function editLessonQuiz(
    lessonId
) {

    try {

        const response =
            await fetch(
                `/admin/api/lesson/${lessonId}/quiz`
            );


        const result =
            await response.json()
                .catch(() => ({}));


        if (!response.ok) {

            throw new Error(
                getErrorMessage(
                    result,
                    "Quiz not found."
                )
            );

        }


        if (
            !result.quiz
        ) {

            throw new Error(
                "Quiz data is not available."
            );

        }


        window.currentEditingQuizLessonId =
            lessonId;


        showEditLessonQuizModal(
            result.quiz
        );

    }

    catch (error) {

        console.error(
            "Edit quiz error:",
            error
        );


        alert(
            error.message ||
            "Failed to load quiz."
        );

    }

}


// ==========================================================
// Show Quiz Modal
// ==========================================================

function showLessonQuizModal(
    quiz
) {

    let modalElement =
        document.getElementById(
            "aiQuizModal"
        );


    if (!modalElement) {

        modalElement =
            document.createElement(
                "div"
            );


        modalElement.id =
            "aiQuizModal";


        modalElement.className =
            "modal fade";


        modalElement.tabIndex =
            -1;


        modalElement.innerHTML = `

            <div class="modal-dialog modal-xl modal-dialog-scrollable">

                <div class="modal-content">

                    <div class="modal-header">

                        <div>

                            <h5 class="modal-title">

                                📝 Quiz

                            </h5>

                        </div>


                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal">

                        </button>

                    </div>


                    <div
                        class="modal-body"
                        id="aiQuizBody">

                    </div>


                    <div class="modal-footer">

                        <button
                            type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal">

                            Close

                        </button>

                    </div>

                </div>

            </div>

        `;


        document.body.appendChild(
            modalElement
        );

    }


    const body =
        document.getElementById(
            "aiQuizBody"
        );


    body.innerHTML =
        renderQuizHtml(
            quiz
        );


    const modal =
        bootstrap.Modal.getOrCreateInstance(
            modalElement
        );


    modal.show();

}


// ==========================================================
// Render Quiz HTML
// ==========================================================

function renderQuizHtml(
    quiz
) {

    const questions =
        Array.isArray(
            quiz.questions
        )
            ? quiz.questions
            : [];


    return `

        <div class="mb-4">

            <h4>

                ${escapeHtml(
                    quiz.title || "Quiz"
                )}

            </h4>


            ${
                quiz.description
                    ? `

                    <p class="text-muted">

                        ${escapeHtml(
                            quiz.description
                        )}

                    </p>

                `
                    : ""
            }


            <div class="d-flex gap-2 flex-wrap">

                <span class="badge bg-primary">

                    ${escapeHtml(
                        quiz.difficulty || ""
                    )}

                </span>


                <span class="badge bg-secondary">

                    Passing Score:
                    ${quiz.passing_score ?? 60}%

                </span>


                <span class="badge bg-info text-dark">

                    ${questions.length}
                    Questions

                </span>

            </div>

        </div>


        ${
            questions.length
                ? questions.map(
                    (question, index) => `

                        <div class="card mb-3">

                            <div class="card-body">

                                <h6 class="fw-bold">

                                    ${index + 1}.
                                    ${escapeHtml(
                                        question.question
                                    )}

                                </h6>


                                <div class="mt-3">

                                    ${renderQuizOption(
                                        "A",
                                        question.option_a
                                    )}

                                    ${renderQuizOption(
                                        "B",
                                        question.option_b
                                    )}

                                    ${renderQuizOption(
                                        "C",
                                        question.option_c
                                    )}

                                    ${renderQuizOption(
                                        "D",
                                        question.option_d
                                    )}

                                </div>


                                <div class="mt-3">

                                    <span class="badge bg-success">

                                        Correct Answer:
                                        ${escapeHtml(
                                            question.correct_answer
                                        )}

                                    </span>

                                </div>


                                ${
                                    question.explanation
                                        ? `

                                        <div class="alert alert-light border mt-3 mb-0">

                                            <strong>
                                                Explanation:
                                            </strong>

                                            ${escapeHtml(
                                                question.explanation
                                            )}

                                        </div>

                                    `
                                        : ""
                                }

                            </div>

                        </div>

                    `
                ).join("")
                : `

                    <div class="alert alert-info">

                        No questions available.

                    </div>

                `
        }

    `;

}


// ==========================================================
// Render Quiz Option
// ==========================================================

function renderQuizOption(
    letter,
    value
) {

    return `

        <div class="border rounded p-2 mb-2">

            <strong>

                ${letter}.

            </strong>

            ${escapeHtml(
                value || ""
            )}

        </div>

    `;

}


// ==========================================================
// Edit Quiz Modal
// ==========================================================

function showEditLessonQuizModal(
    quiz
) {

    let modalElement =
        document.getElementById(
            "editLessonQuizModal"
        );


    if (!modalElement) {

        modalElement =
            document.createElement(
                "div"
            );


        modalElement.id =
            "editLessonQuizModal";


        modalElement.className =
            "modal fade";


        modalElement.tabIndex =
            -1;


        modalElement.innerHTML = `

            <div class="modal-dialog modal-xl modal-dialog-scrollable">

                <div class="modal-content">

                    <div class="modal-header">

                        <h5 class="modal-title">

                            ✏️ Edit Quiz

                        </h5>


                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal">

                        </button>

                    </div>


                    <div class="modal-body">

                        <div class="row">

                            <div class="col-md-8 mb-3">

                                <label class="form-label fw-semibold">

                                    Quiz Title

                                </label>


                                <input
                                    type="text"
                                    id="editQuizTitle"
                                    class="form-control">

                            </div>


                            <div class="col-md-4 mb-3">

                                <label class="form-label fw-semibold">

                                    Difficulty

                                </label>


                                <select
                                    id="editQuizDifficulty"
                                    class="form-select">

                                    <option value="Beginner">
                                        Beginner
                                    </option>

                                    <option value="Intermediate">
                                        Intermediate
                                    </option>

                                    <option value="Advanced">
                                        Advanced
                                    </option>

                                </select>

                            </div>


                            <div class="col-md-8 mb-3">

                                <label class="form-label fw-semibold">

                                    Description

                                </label>


                                <textarea
                                    id="editQuizDescription"
                                    class="form-control"
                                    rows="3">
                                </textarea>

                            </div>


                            <div class="col-md-4 mb-3">

                                <label class="form-label fw-semibold">

                                    Passing Score

                                </label>


                                <input
                                    type="number"
                                    id="editQuizPassingScore"
                                    class="form-control"
                                    min="0"
                                    max="100">

                            </div>

                        </div>


                        <hr>


                        <div id="editQuizQuestionsContainer">

                        </div>

                    </div>


                    <div class="modal-footer">

                        <button
                            type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal">

                            Cancel

                        </button>


                        <button
                            type="button"
                            class="btn btn-primary"
                            id="saveQuizBtn">

                            💾 Save Quiz

                        </button>

                    </div>

                </div>

            </div>

        `;


        document.body.appendChild(
            modalElement
        );


        document.getElementById(
            "saveQuizBtn"
        ).addEventListener(
            "click",
            saveLessonQuiz
        );

    }


    document.getElementById(
        "editQuizTitle"
    ).value =
        quiz.title || "";


    document.getElementById(
        "editQuizDescription"
    ).value =
        quiz.description || "";


    document.getElementById(
        "editQuizDifficulty"
    ).value =
        quiz.difficulty || "Beginner";


    document.getElementById(
        "editQuizPassingScore"
    ).value =
        quiz.passing_score ?? 60;


    window.currentEditingQuiz =
        quiz;


    renderQuizEditQuestions(
        quiz.questions || []
    );


    const modal =
        bootstrap.Modal.getOrCreateInstance(
            modalElement
        );


    modal.show();

}


// ==========================================================
// Render Quiz Edit Questions
// ==========================================================

function renderQuizEditQuestions(
    questions
) {

    const container =
        document.getElementById(
            "editQuizQuestionsContainer"
        );


    if (!container) {

        return;

    }


    if (!questions.length) {

        container.innerHTML = `

            <div class="alert alert-info">

                No questions available.

            </div>

        `;

        return;

    }


    container.innerHTML =
        questions.map(
            (question, index) => `

                <div
                    class="card mb-3 quiz-edit-question"
                    data-question-id="${
                        question.id || ""
                    }">

                    <div class="card-header">

                        <strong>

                            Question ${index + 1}

                        </strong>

                    </div>


                    <div class="card-body">

                        <div class="mb-3">

                            <label class="form-label">

                                Question

                            </label>


                            <textarea
                                class="form-control quiz-question"
                                rows="3">${escapeHtml(
                                    question.question || ""
                                )}</textarea>

                        </div>


                        <div class="row">

                            <div class="col-md-6 mb-3">

                                <label class="form-label">

                                    Option A

                                </label>


                                <input
                                    type="text"
                                    class="form-control quiz-option-a"
                                    value="${escapeAttribute(
                                        question.option_a || ""
                                    )}">

                            </div>


                            <div class="col-md-6 mb-3">

                                <label class="form-label">

                                    Option B

                                </label>


                                <input
                                    type="text"
                                    class="form-control quiz-option-b"
                                    value="${escapeAttribute(
                                        question.option_b || ""
                                    )}">

                            </div>


                            <div class="col-md-6 mb-3">

                                <label class="form-label">

                                    Option C

                                </label>


                                <input
                                    type="text"
                                    class="form-control quiz-option-c"
                                    value="${escapeAttribute(
                                        question.option_c || ""
                                    )}">

                            </div>


                            <div class="col-md-6 mb-3">

                                <label class="form-label">

                                    Option D

                                </label>


                                <input
                                    type="text"
                                    class="form-control quiz-option-d"
                                    value="${escapeAttribute(
                                        question.option_d || ""
                                    )}">

                            </div>


                            <div class="col-md-4 mb-3">

                                <label class="form-label">

                                    Correct Answer

                                </label>


                                <select
                                    class="form-select quiz-correct-answer">

                                    <option
                                        value="A"
                                        ${
                                            question.correct_answer === "A"
                                                ? "selected"
                                                : ""
                                        }>

                                        A

                                    </option>

                                    <option
                                        value="B"
                                        ${
                                            question.correct_answer === "B"
                                                ? "selected"
                                                : ""
                                        }>

                                        B

                                    </option>

                                    <option
                                        value="C"
                                        ${
                                            question.correct_answer === "C"
                                                ? "selected"
                                                : ""
                                        }>

                                        C

                                    </option>

                                    <option
                                        value="D"
                                        ${
                                            question.correct_answer === "D"
                                                ? "selected"
                                                : ""
                                        }>

                                        D

                                    </option>

                                </select>

                            </div>


                            <div class="col-md-8 mb-3">

                                <label class="form-label">

                                    Explanation

                                </label>


                                <input
                                    type="text"
                                    class="form-control quiz-explanation"
                                    value="${escapeAttribute(
                                        question.explanation || ""
                                    )}">

                            </div>

                        </div>

                    </div>

                </div>

            `
        ).join("");

}


// ==========================================================
// Save Quiz
// ==========================================================

async function saveLessonQuiz() {

    const lessonId =
        window.currentEditingQuizLessonId;


    if (!lessonId) {

        alert(
            "Lesson ID is missing."
        );

        return;

    }


    const saveButton =
        document.getElementById(
            "saveQuizBtn"
        );


    const questionCards =
        document.querySelectorAll(
            ".quiz-edit-question"
        );


    const questions = [];


    questionCards.forEach(
        (card, index) => {

            questions.push({

                id:
                    card.dataset.questionId
                        ? Number(
                            card.dataset.questionId
                        )
                        : null,

                question:
                    card.querySelector(
                        ".quiz-question"
                    ).value.trim(),

                option_a:
                    card.querySelector(
                        ".quiz-option-a"
                    ).value.trim(),

                option_b:
                    card.querySelector(
                        ".quiz-option-b"
                    ).value.trim(),

                option_c:
                    card.querySelector(
                        ".quiz-option-c"
                    ).value.trim(),

                option_d:
                    card.querySelector(
                        ".quiz-option-d"
                    ).value.trim(),

                correct_answer:
                    card.querySelector(
                        ".quiz-correct-answer"
                    ).value,

                explanation:
                    card.querySelector(
                        ".quiz-explanation"
                    ).value.trim(),

                display_order:
                    index + 1,

                is_active:
                    true

            });

        }
    );


    const data = {

        title:
            document.getElementById(
                "editQuizTitle"
            ).value.trim(),

        description:
            document.getElementById(
                "editQuizDescription"
            ).value.trim() || null,

        difficulty:
            document.getElementById(
                "editQuizDifficulty"
            ).value,

        passing_score:
            Number(
                document.getElementById(
                    "editQuizPassingScore"
                ).value
            ),

        is_active:
            true,

        questions:
            questions

    };


    if (!data.title) {

        alert(
            "Quiz title is required."
        );

        return;

    }


    if (
        data.passing_score < 0 ||
        data.passing_score > 100
    ) {

        alert(
            "Passing score must be between 0 and 100."
        );

        return;

    }


    if (!questions.length) {

        alert(
            "Quiz must contain at least one question."
        );

        return;

    }


    for (
        let index = 0;
        index < questions.length;
        index++
    ) {

        const question =
            questions[index];


        if (!question.question) {

            alert(
                `Question ${index + 1} is required.`
            );

            return;

        }


        if (!question.option_a) {

            alert(
                `Option A is required for question ${index + 1}.`
            );

            return;

        }


        if (!question.option_b) {

            alert(
                `Option B is required for question ${index + 1}.`
            );

            return;

        }


        if (!question.option_c) {

            alert(
                `Option C is required for question ${index + 1}.`
            );

            return;

        }


        if (!question.option_d) {

            alert(
                `Option D is required for question ${index + 1}.`
            );

            return;

        }

    }


    try {

        saveButton.disabled = true;

        saveButton.innerText =
            "Saving...";


        const response =
            await fetch(
                `/admin/api/lesson/${lessonId}/quiz`,
                {

                    method: "PUT",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify(data)

                }
            );


        const result =
            await response.json()
                .catch(() => ({}));


        if (!response.ok) {

            throw new Error(
                getErrorMessage(
                    result,
                    "Failed to save quiz."
                )
            );

        }


        alert(
            result.message ||
            "Quiz updated successfully."
        );


        const modalElement =
            document.getElementById(
                "editLessonQuizModal"
            );


        const modal =
            bootstrap.Modal.getInstance(
                modalElement
            );


        if (modal) {

            modal.hide();

        }


        await loadCourse();

    }

    catch (error) {

        console.error(
            "Save quiz error:",
            error
        );


        alert(
            error.message ||
            "Failed to save quiz."
        );

    }

    finally {

        saveButton.disabled = false;

        saveButton.innerText =
            "💾 Save Quiz";

    }

}


// ==========================================================
// Array → Text
// ==========================================================

function arrayToText(
    value
) {

    if (!value) {

        return "";

    }


    if (Array.isArray(value)) {

        return value.join("\n");

    }


    return String(value);

}


// ==========================================================
// Array → Code Text
// ==========================================================

function arrayToCodeText(
    value
) {

    if (!value) {

        return "";

    }


    if (Array.isArray(value)) {

        return value.join("\n\n");

    }


    return String(value);

}


// ==========================================================
// Text → Array
// ==========================================================

function textToArray(
    value
) {

    return String(value || "")

        .split("\n")

        .map(
            item =>
                item.trim()
        )

        .filter(
            item =>
                item.length > 0
        );

}


// ==========================================================
// Code Text → Array
// ==========================================================

function codeTextToArray(
    value
) {

    return String(value || "")

        .split(/\n\s*\n/)

        .map(
            item =>
                item.trim()
        )

        .filter(
            item =>
                item.length > 0
        );

}


// ==========================================================
// Show Saved Lesson Content
// ==========================================================

function showLessonContentModal(
    content
) {

    let modalElement =
        document.getElementById(
            "aiLessonContentModal"
        );


    if (!modalElement) {

        modalElement =
            document.createElement(
                "div"
            );


        modalElement.id =
            "aiLessonContentModal";


        modalElement.className =
            "modal fade";


        modalElement.tabIndex =
            -1;


        modalElement.innerHTML = `

            <div class="modal-dialog modal-xl modal-dialog-scrollable">

                <div class="modal-content">

                    <div class="modal-header">

                        <h5 class="modal-title">

                            ✨ AI Generated Lesson Content

                        </h5>


                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal">

                        </button>

                    </div>


                    <div
                        class="modal-body"
                        id="aiLessonContentBody">

                    </div>


                    <div class="modal-footer">

                        <button
                            type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal">

                            Close

                        </button>

                    </div>

                </div>

            </div>

        `;


        document.body.appendChild(
            modalElement
        );

    }


    const body =
        document.getElementById(
            "aiLessonContentBody"
        );


    body.innerHTML = `

        <div class="ai-lesson-content">

            <section class="mb-4">

                <h5 class="fw-bold">

                    📖 Explanation

                </h5>


                <div class="mt-2">

                    ${formatParagraphs(
                        content.explanation
                    )}

                </div>

            </section>


            <section class="mb-4">

                <h5 class="fw-bold">

                    🎯 Learning Objectives

                </h5>


                <div class="mt-2">

                    ${formatList(
                        content.learning_objectives
                    )}

                </div>

            </section>


            <section class="mb-4">

                <h5 class="fw-bold">

                    💡 Examples

                </h5>


                <div class="mt-2">

                    ${formatList(
                        content.examples
                    )}

                </div>

            </section>


            <section class="mb-4">

                <h5 class="fw-bold">

                    💻 Code Examples

                </h5>


                <div class="mt-2">

                    ${formatCodeExamples(
                        content.code_examples
                    )}

                </div>

            </section>


            <section class="mb-4">

                <h5 class="fw-bold">

                    🛠 Practical Exercise

                </h5>


                <div class="alert alert-light border mt-2">

                    ${formatParagraphs(
                        content.practical_exercise
                    )}

                </div>

            </section>


            <section class="mb-2">

                <h5 class="fw-bold">

                    📌 Key Points

                </h5>


                <div class="mt-2">

                    ${formatList(
                        content.key_points
                    )}

                </div>

            </section>

        </div>

    `;


    const modal =
        bootstrap.Modal.getOrCreateInstance(
            modalElement
        );


    modal.show();

}


// ==========================================================
// Format List
// ==========================================================

function formatList(
    value
) {

    if (!value) {

        return `

            <p class="text-muted">

                No content available.

            </p>

        `;

    }


    let items = [];


    if (Array.isArray(value)) {

        items = value;

    }

    else {

        items =
            String(value)
                .split("\n")
                .map(
                    item =>
                        item
                            .replace(
                                /^[-•*]\s*/,
                                ""
                            )
                            .trim()
                )
                .filter(
                    item =>
                        item.length > 0
                );

    }


    if (!items.length) {

        return `

            <p class="text-muted">

                No content available.

            </p>

        `;

    }


    return `

        <ul class="mb-0">

            ${items.map(
                item => `

                    <li class="mb-2">

                        ${escapeHtml(item)}

                    </li>

                `
            ).join("")}

        </ul>

    `;

}


// ==========================================================
// Format Paragraphs
// ==========================================================

function formatParagraphs(
    value
) {

    if (!value) {

        return `

            <p class="text-muted">

                No content available.

            </p>

        `;

    }


    return String(value)

        .split("\n")

        .map(
            paragraph =>
                paragraph.trim()
        )

        .filter(
            paragraph =>
                paragraph.length > 0
        )

        .map(
            paragraph => `

                <p class="mb-2">

                    ${escapeHtml(
                        paragraph
                    )}

                </p>

            `
        )

        .join("");

}


// ==========================================================
// Format Code Examples
// ==========================================================

function formatCodeExamples(
    value
) {

    if (!value) {

        return `

            <p class="text-muted">

                No code examples available.

            </p>

        `;

    }


    let examples = [];


    if (Array.isArray(value)) {

        examples = value;

    }

    else {

        examples =
            String(value)
                .split(/\n\s*\n/)
                .filter(
                    item =>
                        item.trim().length > 0
                );

    }


    if (!examples.length) {

        return `

            <p class="text-muted">

                No code examples available.

            </p>

        `;

    }


    return examples.map(
        code => `

            <pre class="bg-dark text-light p-3 rounded mb-3"><code>${escapeHtml(
                code
            )}</code></pre>

        `
    ).join("");

}


// ==========================================================
// Error Message Helper
// ==========================================================

function getErrorMessage(
    result,
    fallback
) {

    if (!result) {

        return fallback;

    }


    if (
        typeof result.detail === "string"
    ) {

        return result.detail;

    }


    if (
        Array.isArray(result.detail)
    ) {

        return result.detail
            .map(
                item =>
                    item.msg ||
                    item.message ||
                    String(item)
            )
            .join(", ");

    }


    if (
        result.message
    ) {

        return result.message;

    }


    return fallback;

}


// ==========================================================
// Escape JavaScript String
// ==========================================================

function escapeJs(
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
            /\\/g,
            "\\\\"
        )

        .replace(
            /'/g,
            "\\'"
        )

        .replace(
            /"/g,
            '\\"'
        )

        .replace(
            /\n/g,
            "\\n"
        )

        .replace(
            /\r/g,
            "\\r"
        );

}


// ==========================================================
// HTML Escape Helper
// ==========================================================

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


// ==========================================================
// HTML Attribute Escape Helper
// ==========================================================

function escapeAttribute(
    value
) {

    return escapeHtml(
        value
    );

}