/*
==========================================================
PlacementsPro
Global JavaScript
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    console.log("PlacementsPro app.js loaded");

    // =====================================================
    // Mobile Navigation Menu
    // =====================================================

    const mobileMenuBtn =
        document.querySelector(".mobile-menu-btn");

    const navbarContainer =
        document.querySelector(".navbar-container");

    if (mobileMenuBtn && navbarContainer) {

        mobileMenuBtn.addEventListener("click", function () {

            navbarContainer.classList.toggle("mobile-open");

            const isOpen =
                navbarContainer.classList.contains("mobile-open");

            mobileMenuBtn.setAttribute(
                "aria-expanded",
                isOpen
            );

            mobileMenuBtn.setAttribute(
                "aria-label",
                isOpen
                    ? "Close navigation menu"
                    : "Open navigation menu"
            );

            mobileMenuBtn.textContent =
                isOpen ? "✕" : "☰";

        });

    }

    // =====================================================
    // Close Mobile Menu
    // =====================================================

    function closeMobileMenu() {

        if (!navbarContainer || !mobileMenuBtn) {
            return;
        }

        navbarContainer.classList.remove("mobile-open");

        mobileMenuBtn.setAttribute(
            "aria-expanded",
            "false"
        );

        mobileMenuBtn.setAttribute(
            "aria-label",
            "Open navigation menu"
        );

        mobileMenuBtn.textContent = "☰";

    }

    // =====================================================
    // Generic Smooth Scroll
    // =====================================================

    function smoothScrollTo(elementId, offset = 0) {

        const element =
            document.getElementById(elementId);

        if (!element) {

            console.error(`${elementId} not found`);

            return;

        }

        const position =
            element.getBoundingClientRect().top +
            window.pageYOffset +
            offset;

        window.scrollTo({

            top: position,

            behavior: "smooth"

        });

    }

    // =====================================================
    // Courses
    // =====================================================

    const navCourses =
        document.getElementById("navCourses");

    if (navCourses) {

        navCourses.addEventListener("click", function (e) {

            e.preventDefault();

            smoothScrollTo("courses", 2900);

            closeMobileMenu();

        });

    }

    // =====================================================
    // Hero Explore Courses
    // =====================================================

    const exploreCourses =
        document.getElementById("exploreCourses");

    if (exploreCourses) {

        exploreCourses.addEventListener("click", function (e) {

            e.preventDefault();

            smoothScrollTo("courses", 2900);

            closeMobileMenu();

        });

    }

    // =====================================================
    // About
    // =====================================================

    const navAbout =
        document.getElementById("navAbout");

    if (navAbout) {

        navAbout.addEventListener("click", function (e) {

            e.preventDefault();

            smoothScrollTo("about", -50);

            closeMobileMenu();

        });

    }

    // =====================================================
    // Contact
    // =====================================================

    const navContact =
        document.getElementById("navContact");

    if (navContact) {

        navContact.addEventListener("click", function (e) {

            e.preventDefault();

            smoothScrollTo("contact", -50);

            closeMobileMenu();

        });

    }

    // =====================================================
    // Hero Contact Button
    // =====================================================

    const contactUs =
        document.getElementById("contactUs");

    if (contactUs) {

        contactUs.addEventListener("click", function (e) {

            e.preventDefault();

            smoothScrollTo("contact", -50);

            closeMobileMenu();

        });

    }

    // =====================================================
    // Close Menu After Login / Enroll Click
    // =====================================================

    const navButtons =
        document.querySelectorAll(".nav-buttons a");

    navButtons.forEach(button => {

        button.addEventListener("click", function () {

            closeMobileMenu();

        });

    });

});