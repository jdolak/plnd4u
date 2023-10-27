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

function addCourse() {
    const courseName = document.getElementById('course-name').value;
    const courseCode = document.getElementById('course-code').value;
    const overlay = document.getElementById("unlisted-course-overlay-container");
    $.ajax({
        url: '/classes',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({  'course_name': courseName, 'course_code': courseCode    }),
        success: function(response) {
            document.getElementById('unlisted-course-output').innerHTML = response.course_name + ' is a replacement for ' + response.course_code;
        },
        error: function(error) {
            console.log(error);
        }
    })

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

function searchClasses() {
    const searchInput = document.getElementById('search-bar').value;
    $.ajax({ 
        url: '/classes',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify( {'search_input': searchInput }),
        success: function(response) {
            document.getElementById('search-course-output').innerHTML = response.search_output;
        },
        error: function(error) {
            console.log(error);
        }
    })
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        searchClasses();
    }
}