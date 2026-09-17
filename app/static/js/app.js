/*
==========================================================
SkillForge Academy
Global JavaScript
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    console.log("SkillForge app.js loaded");

    // =====================================================
    // Generic Smooth Scroll
    // =====================================================

    function smoothScrollTo(elementId, offset = 0) {

        const element = document.getElementById(elementId);

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

            // Scroll directly to course cards
            smoothScrollTo("courses", 2900);

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

        });

    }

});