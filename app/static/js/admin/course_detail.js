/*
==========================================================
SkillForge LMS
Course Detail
==========================================================
*/

let currentCourse = null;

document.addEventListener(
    "DOMContentLoaded",
    loadCourse
);


// ==========================================================
// Load Course
// ==========================================================

async function loadCourse(){

    const response = await fetch(
        `/admin/api/course/${COURSE_ID}`
    );

    const course = await response.json();

    currentCourse = course;

    renderCourse(course);

}


// ==========================================================
// Render Course
// ==========================================================

function renderCourse(course){

    let html = `

<div class="course-header d-flex justify-content-between align-items-start">

<div>

<h2>

${course.title}

</h2>

<div class="course-meta mt-2">

<span class="badge bg-primary">

${course.level}

</span>

<span class="badge bg-dark">

${course.category}

</span>

<span class="badge bg-warning text-dark">

${course.is_active ? 'Published':'Draft'}

</span>

</div>

</div>

<div>

<button
id="editCourseBtn"
class="btn btn-primary">

<i class="bi bi-pencil-square"></i>

Edit Course

</button>

</div>

</div>

<div
class="accordion"
id="courseAccordion">

`;

    course.modules.forEach((module,index)=>{

        html += `

<div class="accordion-item module-card">

<h2 class="accordion-header">

<button
class="accordion-button ${index ? 'collapsed':''}"
type="button"
data-bs-toggle="collapse"
data-bs-target="#module${module.id}">

${module.title}

</button>

</h2>

<div
id="module${module.id}"
class="accordion-collapse collapse ${index==0?'show':''}">

<div class="accordion-body">

`;

        module.lessons.forEach(lesson=>{

            html += `

<div class="lesson-item d-flex justify-content-between">

<span>

📘 ${lesson.title}

</span>

</div>

`;

        });

        html += `

</div>

</div>

</div>

`;

    });

    html += "</div>";

    document.getElementById(
        "courseContainer"
    ).innerHTML = html;

    document
        .getElementById("editCourseBtn")
        .addEventListener(
            "click",
            openEditModal
        );

}


// ==========================================================
// Open Modal
// ==========================================================

function openEditModal(){

    document.getElementById(
        "courseTitle"
    ).value = currentCourse.title;

    document.getElementById(
        "courseCategory"
    ).value = currentCourse.category;

    document.getElementById(
        "courseLevel"
    ).value = currentCourse.level;

    document.getElementById(
        "courseDuration"
    ).value = currentCourse.duration;

    document.getElementById(
        "coursePrice"
    ).value = currentCourse.price;

    document.getElementById(
        "courseDescription"
    ).value = currentCourse.description;

    const modal = new bootstrap.Modal(
        document.getElementById(
            "editCourseModal"
        )
    );

    modal.show();

}


// ==========================================================
// Save Button
// ==========================================================

document
    .getElementById(
        "saveCourseBtn"
    )
    .addEventListener(
        "click",
        saveCourse
    );


// ==========================================================
// Save Course
// ==========================================================

// ==========================================================
// Save Course
// ==========================================================

async function saveCourse() {

    try {

        const response = await fetch(

            `/admin/api/course/${COURSE_ID}`,

            {

                method: "PUT",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    title: document.getElementById(
                        "courseTitle"
                    ).value,

                    description: document.getElementById(
                        "courseDescription"
                    ).value,

                    category: document.getElementById(
                        "courseCategory"
                    ).value,

                    level: document.getElementById(
                        "courseLevel"
                    ).value,

                    duration: parseInt(
                        document.getElementById(
                            "courseDuration"
                        ).value
                    ),

                    price: parseInt(
                        document.getElementById(
                            "coursePrice"
                        ).value
                    )

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

        bootstrap.Modal.getInstance(

            document.getElementById(
                "editCourseModal"
            )

        ).hide();

        loadCourse();

    }

    catch(error){

        console.error(error);

        alert(error.message);

    }

}