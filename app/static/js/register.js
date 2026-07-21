/*
==========================================================
SkillForge LMS
Register JavaScript
==========================================================
*/

const registerForm = document.getElementById("registerForm");
const messageBox = document.getElementById("message");

registerForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    messageBox.className = "alert d-none";

    const full_name = document.getElementById("full_name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    if (password !== confirmPassword) {

        messageBox.classList.remove("d-none");
        messageBox.classList.add("alert-danger");

        messageBox.innerHTML = "Passwords do not match.";

        return;
    }

    try {

        const response = await fetch("/auth/register", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                full_name,
                email,
                password
            })

        });

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail || "Registration failed."
            );

        }

        messageBox.classList.remove("d-none");
        messageBox.classList.add("alert-success");

        messageBox.innerHTML =
            "✅ Registration successful. Redirecting to Login...";

        setTimeout(() => {

            window.location.href = "/login";

        }, 1500);

    }
    catch (error) {

        messageBox.classList.remove("d-none");
        messageBox.classList.add("alert-danger");

        messageBox.innerHTML = error.message;

    }

});