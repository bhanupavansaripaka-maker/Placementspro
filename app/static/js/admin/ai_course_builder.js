/*
==========================================================
Global State
==========================================================
*/

let generatedCurriculum = null;
/*
==========================================================
SkillForge LMS
AI Content Studio
==========================================================
*/

const generateBtn = document.getElementById("generateBtn");
const loadingArea = document.getElementById("loadingArea");
const resultArea = document.getElementById("curriculumResult");

generateBtn.addEventListener("click", generateCurriculum);

async function generateCurriculum() {

    const courseName = document.getElementById("courseName").value.trim();
    const difficulty = document.getElementById("difficulty").value;
    const duration = document.getElementById("duration").value;
    const audience = document.getElementById("audience").value.trim();

    if (!courseName) {
        alert("Please enter Course Name.");
        return;
    }

    if (!audience) {
        alert("Please enter Target Audience.");
        return;
    }

    generateBtn.disabled = true;

    loadingArea.style.display = "block";

    resultArea.innerHTML = "";

    try {

        const response = await fetch(
            "/api/ai/generate-curriculum",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    course_name: courseName,
                    difficulty: difficulty,
                    duration: duration,
                    target_audience: audience
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail || "Unable to generate curriculum."
            );

        }
        generatedCurriculum = data;
        renderCurriculum(data);

    }

    catch (error) {

        resultArea.innerHTML = `

            <div class="alert alert-danger">

                ${error.message}

            </div>

        `;

    }

    finally {

        loadingArea.style.display = "none";

        generateBtn.disabled = false;

    }

}

function renderCurriculum(curriculum) {

    let html = `

        <div class="card shadow">

            <div class="card-body">

                <div class="d-flex justify-content-between align-items-center mb-4">

                    <div>

                        <h3>

                            📚 ${curriculum.course}

                        </h3>

                        <p class="text-muted">

                            AI Generated Curriculum

                        </p>

                    </div>

                    <div>

                        <button class="btn btn-outline-primary me-2">

                            ✏ Edit

                        <button
                            id="saveCurriculumBtn"
                            class="btn btn-success">

                            💾 Save Curriculum

                        </button>

                    </div>

                </div>

    `;

    curriculum.modules.forEach((module, index) => {

        html += `

            <div class="card mb-4">

                <div class="card-body">

                    <h4>

                        Module ${index + 1}

                    </h4>

                    <h5 class="mt-2">

                        ${module.title}

                    </h5>

                    <p class="text-muted">

                        ${module.description}

                    </p>

                    <div class="mt-4">

        `;

        module.lessons.forEach((lesson) => {

            html += `

                <div class="lesson-item">

                    📘 ${lesson.title}

                </div>

            `;

        });

        html += `

                    </div>

                </div>

            </div>

        `;

    });

    html += `

            </div>

        </div>

    `;

    resultArea.innerHTML = html;
    const saveButton = document.getElementById(
    "saveCurriculumBtn"
);

if (saveButton) {

    saveButton.addEventListener(
        "click",
        saveCurriculum
    );

}
/*
==========================================================
Save Curriculum
==========================================================
*/

async function saveCurriculum() {

    if (!generatedCurriculum) {

        alert("Generate curriculum first.");

        return;

    }

    try {

        const response = await fetch(
            "/admin/api/save-curriculum",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    curriculum: generatedCurriculum,

                    difficulty:
                        document.getElementById(
                            "difficulty"
                        ).value,

                    duration: 90

                })

            }
        );

        const result = await response.json();

        if (!response.ok) {

            throw new Error(
                result.detail
            );

        }

        alert(result.message);

        console.log(result);

    }

    catch (error) {

        console.error(error);

        alert(error.message);

    }

}

}