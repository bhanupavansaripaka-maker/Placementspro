/*
==========================================================
SkillForge LMS
Dashboard API Helper
==========================================================
*/

const DashboardAPI = {

    async getCurrentStudent() {

        if (window.currentStudent) {
            return window.currentStudent;
        }

        const student = await getCurrentStudent();

        if (!student) {
            throw new Error("Unable to load current student.");
        }

        window.currentStudent = student;

        return student;

    },

    async getStatistics() {

        const student = await this.getCurrentStudent();

        const response = await fetch(
            `/api/dashboard/statistics?student_id=${student.id}`
        );

        if (!response.ok) {
            throw new Error("Failed to load statistics.");
        }

        return await response.json();

    },

    async getMyCourses() {

        const student = await this.getCurrentStudent();

        const response = await fetch(
            `/api/enrollments/student/${student.id}`
        );

        if (!response.ok) {
            throw new Error("Failed to load enrolled courses.");
        }

        return await response.json();

    },

    async getContinueLearning() {

        const student = await this.getCurrentStudent();

        const response = await fetch(
            `/api/dashboard/continue-learning?student_id=${student.id}`
        );

        if (!response.ok) {
            throw new Error("Failed to load continue learning.");
        }

        return await response.json();

    }

};