/*
==========================================================
SkillForge LMS
Student Quiz
==========================================================
*/

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadQuiz();

    }
);


/* ==========================================================
   Quiz State
========================================================== */

let quizData = null;

let selectedAnswers = {};

let quizSubmitted = false;


/* ==========================================================
   Load Quiz
========================================================== */

async function loadQuiz() {

    const container =
        document.getElementById(
            "quizContainer"
        );


    if (!container) {

        console.error(
            "quizContainer not found."
        );

        return;

    }


    container.innerHTML = `

        <div class="text-center py-5">

            <div
                class="spinner-border text-primary"
                role="status"
            ></div>

            <h5 class="mt-3">

                Loading Quiz...

            </h5>

            <p class="text-muted">

                Preparing your questions.

            </p>

        </div>

    `;


    try {

        const response = await fetch(
            `/api/quiz/lesson/${LESSON_ID}`
        );


        if (!response.ok) {

            let errorMessage =
                "Unable to load quiz.";

            try {

                const errorData =
                    await response.json();

                errorMessage =
                    errorData.detail ||
                    errorMessage;

            }

            catch (e) {

                console.error(
                    "Unable to read error response.",
                    e
                );

            }


            throw new Error(
                errorMessage
            );

        }


        quizData =
            await response.json();


        selectedAnswers = {};

        quizSubmitted = false;


        renderQuiz(
            quizData
        );

    }

    catch (error) {

        console.error(
            "Quiz loading error:",
            error
        );


        container.innerHTML = `

            <div class="alert alert-danger">

                <h5>

                    Unable to load quiz

                </h5>

                <p class="mb-0">

                    ${escapeHtml(
                        error.message
                    )}

                </p>

                <button
                    class="btn btn-outline-danger mt-3"
                    onclick="loadQuiz()"
                >

                    <i
                        class="bi bi-arrow-repeat me-2"
                    ></i>

                    Try Again

                </button>

            </div>

        `;

    }

}


/* ==========================================================
   Render Quiz
========================================================== */

function renderQuiz(
    quiz
) {

    const title =
        document.getElementById(
            "quizTitle"
        );


    const description =
        document.getElementById(
            "quizDescription"
        );


    const difficulty =
        document.getElementById(
            "quizDifficulty"
        );


    if (title) {

        title.textContent =
            quiz.title || "Quiz";

    }


    if (description) {

        description.textContent =
            quiz.description || "";

    }


    if (difficulty) {

        difficulty.textContent =
            quiz.difficulty || "Beginner";

    }


    const questions =
        quiz.questions || [];


    if (questions.length === 0) {

        document.getElementById(
            "quizContainer"
        ).innerHTML = `

            <div class="alert alert-warning">

                <h5>

                    No Questions Available

                </h5>

                <p class="mb-0">

                    There are currently no questions
                    available for this quiz.

                </p>

            </div>

        `;

        return;

    }


    updateProgress(
        questions.length
    );


    const container =
        document.getElementById(
            "quizContainer"
        );


    let html = "";


    questions.forEach(
        (question, index) => {

            html += renderQuestion(
                question,
                index
            );

        }
    );


    /* ------------------------------------------------------
       Submit Section
    ------------------------------------------------------ */

    html += `

        <div
            class="card shadow-sm mb-4"
        >

            <div class="card-body">

                <div
                    class="d-flex
                           justify-content-between
                           align-items-center
                           flex-wrap
                           gap-3"
                >

                    <div>

                        <strong>

                            Passing Score:

                        </strong>

                        ${quiz.passing_score || 60}%

                    </div>


                    <button
                        id="submitQuizBtn"
                        class="btn btn-primary btn-lg"
                    >

                        <i
                            class="bi bi-check-circle me-2"
                        ></i>

                        Submit Quiz

                    </button>

                </div>

            </div>

        </div>

    `;


    container.innerHTML =
        html;


    attachAnswerHandlers();


    const submitButton =
        document.getElementById(
            "submitQuizBtn"
        );


    if (submitButton) {

        submitButton.addEventListener(
            "click",
            submitQuiz
        );

    }

}


/* ==========================================================
   Render Individual Question
========================================================== */

function renderQuestion(
    question,
    index
) {

    const selectedAnswer =
        selectedAnswers[
            String(question.id)
        ];


    return `

        <div
            class="card shadow-sm mb-4"
        >

            <div class="card-body">

                <div
                    class="d-flex
                           align-items-start"
                >

                    <span
                        class="badge bg-primary
                               me-3 fs-6"
                    >

                        ${index + 1}

                    </span>


                    <h5
                        class="fw-semibold mb-0"
                    >

                        ${escapeHtml(
                            question.question
                        )}

                    </h5>

                </div>


                <div class="mt-4">

                    ${renderOption(
                        question,
                        "A",
                        selectedAnswer
                    )}

                    ${renderOption(
                        question,
                        "B",
                        selectedAnswer
                    )}

                    ${renderOption(
                        question,
                        "C",
                        selectedAnswer
                    )}

                    ${renderOption(
                        question,
                        "D",
                        selectedAnswer
                    )}

                </div>

            </div>

        </div>

    `;

}


/* ==========================================================
   Render Option
========================================================== */

function renderOption(
    question,
    option,
    selectedAnswer
) {

    const optionText =
        question[
            `option_${option.toLowerCase()}`
        ] || "";


    const isChecked =
        selectedAnswer === option
            ? "checked"
            : "";


    return `

        <label
            class="d-block
                   border
                   rounded
                   p-3
                   mb-3
                   option-label"
            style="cursor: pointer;"
        >

            <div class="form-check">

                <input
                    class="form-check-input
                           answer-option"
                    type="radio"
                    name="question_${question.id}"
                    value="${option}"
                    data-question-id="${question.id}"
                    ${isChecked}
                >


                <span
                    class="form-check-label"
                >

                    <strong>

                        ${option}.

                    </strong>

                    ${escapeHtml(
                        optionText
                    )}

                </span>

            </div>

        </label>

    `;

}


/* ==========================================================
   Attach Answer Handlers
========================================================== */

function attachAnswerHandlers() {

    const options =
        document.querySelectorAll(
            ".answer-option"
        );


    options.forEach(
        option => {

            option.addEventListener(
                "change",
                () => {

                    if (quizSubmitted) {

                        return;

                    }


                    const questionId =
                        option.dataset.questionId;


                    selectedAnswers[
                        questionId
                    ] = option.value;


                    updateAnsweredProgress();

                    updateOptionStyles(
                        questionId
                    );

                }
            );

        }
    );


    updateAnsweredProgress();

}


/* ==========================================================
   Update Option Styles
========================================================== */

function updateOptionStyles(
    questionId
) {

    const selected =
        selectedAnswers[
            questionId
        ];


    const options =
        document.querySelectorAll(
            `[data-question-id="${questionId}"]`
        );


    options.forEach(
        option => {

            const label =
                option.closest(
                    ".option-label"
                );


            if (!label) {

                return;

            }


            if (
                option.value === selected
            ) {

                label.classList.add(
                    "border-primary"
                );

            }

            else {

                label.classList.remove(
                    "border-primary"
                );

            }

        }
    );

}


/* ==========================================================
   Update Initial Progress
========================================================== */

function updateProgress(
    totalQuestions
) {

    const progressText =
        document.getElementById(
            "progressText"
        );


    const progressBar =
        document.getElementById(
            "progressBar"
        );


    if (!progressText ||
        !progressBar) {

        return;

    }


    progressText.textContent =
        `0 / ${totalQuestions}`;


    progressBar.style.width =
        "0%";


    progressBar.setAttribute(
        "aria-valuenow",
        "0"
    );

}


/* ==========================================================
   Update Answered Progress
========================================================== */

function updateAnsweredProgress() {

    if (!quizData) {

        return;

    }


    const questions =
        quizData.questions || [];


    const total =
        questions.length;


    const answered =
        Object.keys(
            selectedAnswers
        ).length;


    const percentage =
        total > 0
            ? Math.round(
                (
                    answered /
                    total
                ) * 100
            )
            : 0;


    const progressText =
        document.getElementById(
            "progressText"
        );


    const progressBar =
        document.getElementById(
            "progressBar"
        );


    if (progressText) {

        progressText.textContent =
            `${answered} / ${total}`;

    }


    if (progressBar) {

        progressBar.style.width =
            `${percentage}%`;


        progressBar.setAttribute(
            "aria-valuenow",
            String(percentage)
        );

    }

}


/* ==========================================================
   Submit Quiz
========================================================== */

async function submitQuiz() {

    if (!quizData ||
        quizSubmitted) {

        return;

    }


    const questions =
        quizData.questions || [];


    const totalQuestions =
        questions.length;


    const answeredQuestions =
        Object.keys(
            selectedAnswers
        ).length;


    /* ------------------------------------------------------
       Confirm Incomplete Quiz
    ------------------------------------------------------ */

    if (
        answeredQuestions <
        totalQuestions
    ) {

        const proceed =
            confirm(
                `You answered ${answeredQuestions} `
                + `out of ${totalQuestions} questions.\n\n`
                + `Do you want to submit anyway?`
            );


        if (!proceed) {

            return;

        }

    }


    /* ------------------------------------------------------
       Confirm Submission
    ------------------------------------------------------ */

    const confirmSubmit =
        confirm(
            "Are you sure you want to submit the quiz?"
        );


    if (!confirmSubmit) {

        return;

    }


    const submitButton =
        document.getElementById(
            "submitQuizBtn"
        );


    if (submitButton) {

        submitButton.disabled =
            true;


        submitButton.innerHTML = `

            <span
                class="spinner-border
                       spinner-border-sm
                       me-2"
            ></span>

            Submitting...

        `;

    }


    try {

        const token =
    localStorage.getItem("access_token");

if (!token) {

    alert(
        "Please login again."
    );

    window.location.href = "/login";

    return;

}


const response = await fetch(
    `/api/quiz/${quizData.id}/submit`,
    {
        method: "POST",

        headers: {
            "Content-Type":
                "application/json",

            "Authorization":
                `Bearer ${token}`
        },

        body: JSON.stringify(
            selectedAnswers
        )
    }
);


        let result;


        try {

            result =
                await response.json();

        }

        catch (e) {

            throw new Error(
                "Invalid response received from server."
            );

        }


        if (!response.ok) {

            throw new Error(
                result.detail ||
                "Unable to submit quiz."
            );

        }


        quizSubmitted = true;


        renderResult(
            result
        );

    }

    catch (error) {

        console.error(
            "Quiz submission error:",
            error
        );


        alert(
            error.message
        );


        if (submitButton) {

            submitButton.disabled =
                false;


            submitButton.innerHTML = `

                <i
                    class="bi bi-check-circle me-2"
                ></i>

                Submit Quiz

            `;

        }

    }

}


/* ==========================================================
   Render Result
========================================================== */

function renderResult(
    result
) {

    const quizContainer =
        document.getElementById(
            "quizContainer"
        );


    const progressContainer =
        document.getElementById(
            "quizProgressContainer"
        );


    const resultContainer =
        document.getElementById(
            "resultContainer"
        );


    if (quizContainer) {

        quizContainer.classList.add(
            "d-none"
        );

    }


    if (progressContainer) {

        progressContainer.classList.add(
            "d-none"
        );

    }


    if (!resultContainer) {

        return;

    }


    resultContainer.classList.remove(
        "d-none"
    );


    const resultClass =
        result.passed
            ? "success"
            : "danger";


    const resultIcon =
        result.passed
            ? "bi-trophy-fill"
            : "bi-arrow-repeat";


    let resultMessage;


    if (result.passed) {

        resultMessage =
            "Congratulations! You passed the quiz.";

    }

    else {

        resultMessage =
            "You did not pass this time. Review the lesson and try again.";

    }


    const courseId =
        getCourseId();


    const backButton =
        courseId
            ? `

                <a
                    href="/learn/${courseId}"
                    class="btn btn-outline-primary me-2"
                >

                    <i
                        class="bi bi-arrow-left me-2"
                    ></i>

                    Back to Course

                </a>

              `
            : `

                <button
                    type="button"
                    id="backToLessonBtn"
                    class="btn btn-outline-primary me-2"
                >

                    <i
                        class="bi bi-arrow-left me-2"
                    ></i>

                    Back

                </button>

              `;


    const html = `

        <div
            class="card shadow-sm mb-4"
        >

            <div
                class="card-body
                       text-center
                       py-5"
            >

                <i
                    class="bi ${resultIcon}
                           fs-1
                           text-${resultClass}"
                ></i>


                <h2
                    class="fw-bold mt-3"
                >

                    ${
                        result.passed
                            ? "Quiz Passed!"
                            : "Quiz Not Passed"
                    }

                </h2>


                <div
                    class="display-4
                           fw-bold
                           text-${resultClass}"
                >

                    ${result.score}%

                </div>


                <p class="text-muted">

                    ${result.correct_answers}

                    out of

                    ${result.total_questions}

                    answers correct

                </p>


                <p>

                    Passing score:

                    <strong>

                        ${result.passing_score}%

                    </strong>

                </p>


                <p class="text-muted">

                    ${escapeHtml(
                        resultMessage
                    )}

                </p>


                <div class="mt-4">

                    ${backButton}


                    <button
                        id="retryQuizBtn"
                        class="btn btn-primary"
                    >

                        <i
                            class="bi bi-arrow-repeat me-2"
                        ></i>

                        Retry Quiz

                    </button>

                </div>

            </div>

        </div>


        <div
            class="card shadow-sm"
        >

            <div class="card-header">

                <h5 class="mb-0">

                    <i
                        class="bi bi-list-check me-2"
                    ></i>

                    Answer Review

                </h5>

            </div>


            <div class="card-body">

                ${renderAnswerReview(
                    result.results
                )}

            </div>

        </div>

    `;


    resultContainer.innerHTML =
        html;


    /* ------------------------------------------------------
       Retry
    ------------------------------------------------------ */

    const retryButton =
        document.getElementById(
            "retryQuizBtn"
        );


    if (retryButton) {

        retryButton.addEventListener(
            "click",
            () => {

                location.reload();

            }
        );

    }


    /* ------------------------------------------------------
       Back
    ------------------------------------------------------ */

    const backToLessonButton =
        document.getElementById(
            "backToLessonBtn"
        );


    if (backToLessonButton) {

        backToLessonButton.addEventListener(
            "click",
            () => {

                window.history.back();

            }
        );

    }

}


/* ==========================================================
   Render Answer Review
========================================================== */

function renderAnswerReview(
    results
) {

    if (
        !results ||
        results.length === 0
    ) {

        return `

            <p class="text-muted mb-0">

                No answer details available.

            </p>

        `;

    }


    return results.map(
        (result, index) => {

            const statusClass =
                result.is_correct
                    ? "success"
                    : "danger";


            const statusIcon =
                result.is_correct
                    ? "bi-check-circle-fill"
                    : "bi-x-circle-fill";


            const submitted =
                result.submitted_answer
                    || "Not answered";


            return `

                <div
                    class="border rounded p-3 mb-3"
                >

                    <div class="d-flex">

                        <i
                            class="bi ${statusIcon}
                                   text-${statusClass}
                                   fs-5 me-2"
                        ></i>


                        <div
                            class="flex-grow-1"
                        >

                            <div class="fw-semibold">

                                ${index + 1}.

                                ${escapeHtml(
                                    result.question
                                )}

                            </div>


                            <div class="mt-2">

                                Your answer:

                                <strong>

                                    ${escapeHtml(
                                        submitted
                                    )}

                                </strong>

                            </div>


                            <div>

                                Correct answer:

                                <strong>

                                    ${escapeHtml(
                                        result.correct_answer
                                    )}

                                </strong>

                            </div>


                            ${
                                result.explanation
                                    ? `

                                        <div
                                            class="alert
                                                   alert-light
                                                   mt-3
                                                   mb-0"
                                        >

                                            <strong>

                                                Explanation:

                                            </strong>


                                            <div class="mt-1">

                                                ${escapeHtml(
                                                    result.explanation
                                                )}

                                            </div>

                                        </div>

                                      `
                                    : ""
                            }

                        </div>

                    </div>

                </div>

            `;

        }
    ).join("");

}


/* ==========================================================
   Get Course ID
========================================================== */

function getCourseId() {

    /*
    We first check whether the
    course ID was provided by quiz.html.
    */


    if (
        typeof COURSE_ID !==
        "undefined"
    ) {

        return COURSE_ID;

    }


    /*
    If COURSE_ID is not available,
    try to get it from the page.
    */


    const courseElement =
        document.getElementById(
            "courseId"
        );


    if (
        courseElement &&
        courseElement.value
    ) {

        return courseElement.value;

    }


    /*
    No course ID available.
    */

    return "";

}


/* ==========================================================
   Escape HTML
========================================================== */

function escapeHtml(
    value
) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        value ?? "";


    return div.innerHTML;

}