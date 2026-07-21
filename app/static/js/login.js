/*
==========================================================
SkillForge LMS
Login JavaScript
==========================================================
*/

const loginForm = document.getElementById("loginForm");
const messageBox = document.getElementById("message");

loginForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    messageBox.className = "alert d-none";

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {

        const response = await fetch("/auth/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email,
                password
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Invalid email or password.");
        }

        // Save JWT Token
        localStorage.setItem(
            "access_token",
            data.access_token
        );

        localStorage.setItem(
            "token_type",
            data.token_type
        );

        messageBox.classList.remove("d-none");
        messageBox.classList.add("alert-success");

        messageBox.innerHTML =
            "✅ Login successful. Redirecting...";

        setTimeout(() => {

            // Dashboard will be created next
            window.location.href = "/dashboard";

        }, 1000);

    }
    catch (error) {

        messageBox.classList.remove("d-none");
        messageBox.classList.add("alert-danger");

        messageBox.innerHTML = error.message;

    }

});