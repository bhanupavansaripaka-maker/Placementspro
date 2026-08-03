/*
==========================================================
SkillForge LMS
AI Course Builder
==========================================================
*/

const generateBtn = document.getElementById("generateBtn");
const resultContainer = document.getElementById("curriculumResult");

generateBtn.addEventListener("click", async () => {

    const courseName = document.getElementById("courseName").value.trim();
    const difficulty = document.getElementById("difficulty").value;
    const duration = document.getElementById("duration").value;
    const audience = document.getElementById("audience").value.trim();

    if (!courseName) {

        alert("Please enter a course name.");

        return;
    }

    if (!audience) {

        alert("Please enter the target audience.");

        return;
    }

    generateBtn.disabled = true;

    generateBtn.innerHTML = `
        <span class="spinner-border spinner-border-sm"></span>
        Generating Curriculum...
    `;

    resultContainer.innerHTML = `
        <div class="alert alert-info">
            🤖 AI is generating a professional curriculum...
        </div>
    `;

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

        renderCurriculum(data);

    }
    catch (error) {

        resultContainer.innerHTML = `
            <div class="alert alert-danger">
                ${error.message}
            </div>
        `;

    }
    finally {

        generateBtn.disabled = false;

        generateBtn.innerHTML = `
            <i class="bi bi-stars"></i>
            Generate Curriculum
        `;

    }

});


function renderCurriculum(curriculum) {

    let html = `

        <div class="card shadow-sm border-0">

            <div class="card-body">

                <h3 class="mb-4">

                    📘 ${curriculum.course}

                </h3>

    `;

    curriculum.modules.forEach((module, index) => {

        html += `

            <div class="card mb-4">

                <div class="card-body">

                    <h4>

                        Module ${index + 1}

                    </h4>

                    <h5>

                        ${module.title}

                    </h5>

                    <p>

                        ${module.description}

                    </p>

                    <ul class="list-group">

        `;

        module.lessons.forEach((lesson) => {

            html += `

                <li class="list-group-item">

                    📚 ${lesson.title}

                </li>

            `;

        });

        html += `

                    </ul>

                </div>

            </div>

        `;

    });

    html += `

            </div>

        </div>

    `;

    resultContainer.innerHTML = html;

}