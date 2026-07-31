/*
==========================================================
SkillForge LMS
Student Profile
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    loadProfile();

    document
        .getElementById("profileForm")
        .addEventListener("submit", saveProfile);

});


/* ==========================================================
   Load Profile
========================================================== */

async function loadProfile() {

    try {

        const token = localStorage.getItem("access_token");

        const response = await fetch("/students/profile", {

            method: "GET",

            headers: {
                "Authorization": `Bearer ${token}`
            }

        });

        if (!response.ok) {

            throw new Error("Unable to load profile.");

        }

        const profile = await response.json();

        populateProfile(profile);

    }

    catch (error) {

        console.error(error);

        alert("Failed to load profile.");

    }

}


/* ==========================================================
   Populate Profile
========================================================== */

function populateProfile(profile) {

    document.getElementById("profileName").textContent =
        profile.full_name;

    document.getElementById("profileEmail").textContent =
        profile.email;

    document.getElementById("phone").value =
        profile.phone || "";

    document.getElementById("college").value =
        profile.college || "";

    document.getElementById("education").value =
        profile.education || "";

    document.getElementById("branch").value =
        profile.branch || "";

    document.getElementById("graduationYear").value =
        profile.graduation_year || "";

    // Avatar

    const avatar = document.getElementById("profileImage");

    avatar.src =
        `https://ui-avatars.com/api/?name=${encodeURIComponent(profile.full_name)}&background=2563eb&color=ffffff&size=180`;

}


/* ==========================================================
   Save Profile
========================================================== */

async function saveProfile(event) {

    event.preventDefault();

    try {

        const token = localStorage.getItem("access_token");

        const payload = {

            phone:
                document.getElementById("phone").value,

            college:
                document.getElementById("college").value,

            education:
                document.getElementById("education").value,

            branch:
                document.getElementById("branch").value,

            graduation_year:
                parseInt(
                    document.getElementById("graduationYear").value
                ) || null,

            profile_photo: null,

            resume: null

        };

        const response = await fetch("/students/profile", {

            method: "PUT",

            headers: {

                "Content-Type": "application/json",

                "Authorization": `Bearer ${token}`

            },

            body: JSON.stringify(payload)

        });

        if (!response.ok) {

            throw new Error("Unable to update profile.");

        }

        const updatedProfile = await response.json();

        populateProfile(updatedProfile);

        alert("Profile updated successfully.");

    }

    catch (error) {

        console.error(error);

        alert("Failed to update profile.");

    }

}