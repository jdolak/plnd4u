var globalNetId = "";

function addCourse() {
    const courseName = document.getElementById('course-name').value;
    const courseCode = document.getElementById('course-code').value;
    const overlay = document.getElementById("unlisted-course-overlay-container");
    $.ajax({
        url: '/classes',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({  'action': 'add', 'course_name': courseName, 'course_code': courseCode, 'global_netid': globalNetId    }),
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
    globalNetId = netid;
    const password = document.getElementById('pw').value;
    $.ajax({ 
        url: '/login', 
        type: 'POST', 
        contentType: 'application/json', 
        data: JSON.stringify({ 'netid': netid , 'pw' : password}), 
        success: function(response) {
            if (response.status == 0) {
                window.location.replace("/home");
            } else if (response.status == 1){
                document.getElementById('login-output').innerHTML = "Password does not match"
            } else if (response.status == 3){
                document.getElementById('login-output').innerHTML = "User not registered"
            } else {
                document.getElementById('login-output').innerHTML = "error."
            }
        }, 
        error: function(error) {  
            console.log(error); 
        } 
    }); 
}

function sendRegisterData() { 
    const first_name = document.getElementById('first_name').value; 
    const last_name = document.getElementById('last_name').value; 
    const grad = document.getElementById('grad').value; 
    const major = document.getElementById('major').value; 
    const netid = document.getElementById('netid').value; 
    const pw = document.getElementById('pw').value; 
    $.ajax({ 
        url: '/register', 
        type: 'POST', 
        contentType: 'application/json', 
        data: JSON.stringify({ 'first_name' : first_name, 'last_name' : last_name, 'grad' : grad, 'major' : major, 'netid': netid, 'pw' : pw }), 
        success: function(response) { 
            if (response.status == 0) {
                window.location.replace("/home");
            } else if (response.status == 1){
                document.getElementById('register-output').innerHTML = "User account already exists."
            } else {
                document.getElementById('register-output').innerHTML = "error."
            }
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

function addToPlan(className) {
    const overlay = document.getElementById('add-to-plan-overlay-container');
    const content = document.getElementById('add-to-plan-overlay-content');
    const courseHeading = document.querySelector('.add-to-plan-course-heading');

    courseHeading.textContent = className;

    overlay.style.display = 'block';

    const addButton = document.getElementById('add-to-plan-button');
    addButton.addEventListener('click', function() {
        const year = document.getElementById('add-course-year').value;
        const semester = document.getElementById('add-course-semester').value;

        $.ajax({
            url: '/classes',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({  'action': 'add_to_plan', 'year': year, 'semester': semester, 'course': className, 'global_netid': globalNetId   }),
            success: function(response) {
                console.log('success');
            },
            error: function(error) {
                console.log(error);
            }
        })

        overlay.style.display = 'none';
    });

    document.body.addEventListener('click', function(event) {
        if (event.target === overlay && !content.contains(event.target)) {
            overlay.style.display = "none";
        }
    });
}

function getEnrollmentsData() {
    $.ajax({
        url: '/getdata',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            showInPlan(data.enrollments);
        },
        error: function (error) {
            console.error('Error fetching enrollments:', error);
        }
    });
}

function showInPlan(enrollments) {
    const planCardContainer = document.getElementById("unlisted-courses-plan-card-container");

    enrollments.forEach(function (enrollment) {
        const courseCode = enrollment[1];
        const courseName = enrollment[3];

        const courseCard = document.createElement('div');
        courseCard.className = "plan-card-single-course";
    
        const courseCardContent = document.createElement("div");
        courseCardContent.className = "plan-card-single-course-content";
    
        const courseCardContentText = document.createElement("div");
        courseCardContentText.className = "plan-card-single-course-text";
    
        const courseCodeElement = document.createElement("h4");
        courseCodeElement.className = "plan-card-single-course-code";
        courseCodeElement.textContent = courseCode;
    
        const courseNameElement = document.createElement("p");
        courseNameElement.className = "plan-card-single-course-name";
        courseNameElement.textContent = courseName;
    
        const removeButton = document.createElement("button");
        removeButton.className = "remove-button";
        removeButton.innerHTML = '<img src="../static/images/remove.svg">';
    
        courseCardContentText.appendChild(courseCodeElement);
        courseCardContentText.appendChild(courseNameElement);
        courseCardContent.appendChild(courseCardContentText);
        courseCardContent.appendChild(removeButton);
        courseCard.appendChild(courseCardContent);
    
        planCardContainer.appendChild(courseCard);
    });
}


$(document).ready(function() {
    getEnrollmentsData();
});

function searchClasses() {
    const searchInput = document.getElementById('search-bar').value;
    
    const fallSemesterCheckbox = document.querySelector('input[name="fall-semester"]');
    const springSemesterCheckbox = document.querySelector('input[name="spring-semester"]');
    const levelOneCheckbox = document.querySelector('input[name="10000"]');
    const levelTwoCheckbox = document.querySelector('input[name="20000"]');
    const levelThreeCheckbox = document.querySelector('input[name="30000"]');
    const levelFourCheckbox = document.querySelector('input[name="40000"]');
    const uniReqCheckbox = document.querySelector('input[name="uni-req"]');
    const majorReqCheckbox = document.querySelector('input[name="major-req"]');
    const majorElectiveCheckbox = document.querySelector('input[name="major-elective"]');

    const filterData = {
        'fall-semester': fallSemesterCheckbox.checked,
        'spring-semester': springSemesterCheckbox.checked,
        '10000': levelOneCheckbox.checked,
        '20000': levelTwoCheckbox.checked,
        '30000': levelThreeCheckbox.checked,
        '40000': levelFourCheckbox.checked,
        'uni-req': uniReqCheckbox.checked,
        'major-req': majorReqCheckbox.checked,
        'major-elective': majorElectiveCheckbox.checked
    }

    $.ajax({ 
        url: '/classes',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({  'action': 'search', 'search_input': searchInput, 'filter_data': filterData }),
        success: function(response) {

            const searchOutputContainer = document.getElementById('class-database-container');
            searchOutputContainer.innerHTML = '';

            response.search_output.forEach(function (item) {
                const classDiv = searchClassElement(item[0], item[1]);
                searchOutputContainer.appendChild(classDiv);

                classDiv.querySelector('.add-button').addEventListener('click', function() {
                    addToPlan(item[0]);
                });
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

function courseDel() {
    $.ajax({ 
        url: '/plan',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'global_netid': globalNetId }),
        success: function(response) {
            console.log('success');
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function removeCourse(courseId) {
    const courseElement = document.getElementById(courseId);
    if (courseElement) {
        courseElement.remove();
    }
}


// Overlays

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

document.addEventListener("DOMContentLoaded", function() {
    const button = document.getElementById("semester-filter");
    const overlay = document.getElementById("semester-filter-overlay-container");

    button.addEventListener("click", function() {
        const buttonRect = document.getElementById("semester-filter-container").getBoundingClientRect();
        const containerTop = buttonRect.bottom + window.scrollY;
        const containerLeft = buttonRect.left + window.scrollX;

        overlay.style.top = `${containerTop}px`;
        overlay.style.left = `${containerLeft}px`;

        if (overlay.style.display === "block") {
            overlay.style.display = "none";
        } else {
            overlay.style.display = "block";
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const button = document.getElementById("level-filter");
    const overlay = document.getElementById("level-filter-overlay-container");

    button.addEventListener("click", function() {
        const buttonRect = document.getElementById("level-filter-container").getBoundingClientRect();
        const containerTop = buttonRect.bottom + window.scrollY;
        const containerLeft = buttonRect.left + window.scrollX;

        overlay.style.top = `${containerTop}px`;
        overlay.style.left = `${containerLeft}px`;

        if (overlay.style.display === "block") {
            overlay.style.display = "none";
        } else {
            overlay.style.display = "block";
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const button = document.getElementById("req-filter");
    const overlay = document.getElementById("req-filter-overlay-container");

    button.addEventListener("click", function() {
        const buttonRect = document.getElementById("req-filter-container").getBoundingClientRect();
        const containerTop = buttonRect.bottom + window.scrollY;
        const containerLeft = buttonRect.left + window.scrollX;

        overlay.style.top = `${containerTop}px`;
        overlay.style.left = `${containerLeft}px`;

        if (overlay.style.display === "block") {
            overlay.style.display = "none";
        } else {
            overlay.style.display = "block";
        }
    });
});


