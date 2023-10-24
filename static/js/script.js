function createCourseOverlayOn() {
    const overlay = document.getElementById("unlisted-course-overlay-container");
    overlay.style.display = "block";
}

function createCourseOverlayOff(event) {
    const overlay = document.getElementById("unlisted-course-overlay-container");
    const content = document.getElementById("unlisted-course-overlay-content");

    if (event.target === overlay && !content.contains(event.target)) {
        overlay.style.display = "none";
    }
}

const userInputs = [];

function addCourse() {
    const courseNameInput = document.querySelector(".unlisted-text-input[name='course-name']");
    const creditsFulfilledInput = document.querySelector(".unlisted-text-input[name='credits-fulfilled']");
    const userInputDisplay = document.getElementById("user-input-display");
    const overlay = document.getElementById("unlisted-course-overlay-container");

    const courseName = courseNameInput.value; 
    const creditsFulfilled = creditsFulfilledInput.value;

    userInputs.push({courseName, creditsFulfilled});

    courseNameInput.value = "";
    creditsFulfilledInput.value = "";

    let displayContent = '';
    for (let i = 0; i < userInputs.length; i++) {
        displayContent += `Course Name: ${userInputs[i].courseName}, Credits Fulfilled: ${userInputs[i].creditsFulfilled}<br>`;
    }
    userInputDisplay.innerHTML = displayContent;

    overlay.style.display = "none";
}
