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
            console.log('success');
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

function searchClassElement(classCourse, className) {
    const eachClass = document.createElement('div');
    eachClass.classList.add('each-class');

    const textContainer = document.createElement('div');
    textContainer.classList.add('class-text-container');

    const heading = document.createElement('h2');
    heading.classList.add('class-heading');
    heading.textContent = classCourse;

    const normalTextNode = document.createElement('p');
    normalTextNode.classList.add('normal-text');
    normalTextNode.textContent = className;

    textContainer.appendChild(heading);
    textContainer.appendChild(normalTextNode);

    const addButton = document.createElement('button');
    addButton.classList.add('add-button');
    addButton.textContent = 'Add';

    const img = document.createElement('img');
    img.src = '../static/images/add.svg';

    addButton.appendChild(img);

    eachClass.appendChild(textContainer);
    eachClass.appendChild(addButton);

    return eachClass;
}

function searchClasses() {
    const searchInput = document.getElementById('search-bar').value;
    $.ajax({ 
        url: '/classes',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify( {'search_input': searchInput }),
        success: function(response) {

            const searchOutputContainer = document.getElementById('class-database-container');
            searchOutputContainer.innerHTML = '';

            response.search_output.forEach(function (item) {
                const classDiv = searchClassElement(item[0], item[1]);
                searchOutputContainer.appendChild(classDiv);
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        searchClasses();
    }
}