document.addEventListener(
    "DOMContentLoaded",
    loadCourses
);

async function loadCourses(){

    const response =
        await fetch("/admin/api/courses");

    const courses =
        await response.json();

    let html = "";

    courses.forEach(course=>{

        html += `

        <tr>

            <td>

                <strong>

                    ${course.title}

                </strong>

            </td>

            <td>

                ${course.category}

            </td>

            <td>

                ${course.level}

            </td>

            <td>

                ${course.duration} Days

            </td>

            <td>

                <span class="status-badge ${course.is_active ? 'status-active':'status-draft'}">

                    ${course.is_active ? 'Published':'Draft'}

                </span>

            </td>

            <td>

                <a
                    href="/admin/course/${course.id}"
                    class="btn btn-sm btn-primary">

                    View

                </a>

            </td>

        </tr>

        `;

    });

    document.getElementById(
        "courseTableBody"
    ).innerHTML = html;

}