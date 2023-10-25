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
    const equivalentCourseInput = document.querySelector(".unlisted-text-input[name='eq-course']");
    const userInputDisplay = document.getElementById("user-input-display");
    const overlay = document.getElementById("unlisted-course-overlay-container");

    const courseName = courseNameInput.value; 
    const equivalentCourse = equivalentCourseInput.value;

    userInputs.push({courseName, equivalentCourse});

    let displayContent = '';
    for (let i = 0; i < userInputs.length; i++) {
        displayContent += `Course Name: ${userInputs[i].courseName}, Equivalent Course: ${userInputs[i].equivalentCourse}<br>`;
    }
    userInputDisplay.innerHTML = displayContent;

    courseNameInput.value = "";
    equivalentCourseInput.value = "";

    overlay.style.display = "none";
}

function sendLoginData() { 
    const netid = document.getElementById('netid').value; 
    const password = document.getElementById('pw').value;
    $.ajax({ 
        url: '/login', 
        type: 'POST', 
        contentType: 'application/json', 
        data: JSON.stringify({ 'netid': netid }), 
        success: function(response) { 
            document.getElementById('login-output').innerHTML = response.netid; 
        }, 
        error: function(error) { 
            console.log(error); 
        } 
    }); 
} 