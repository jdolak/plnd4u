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
            window.location.reload();
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
                window.location.replace("/plan");
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

    eachClass.style.cursor = 'pointer';

    eachClass.addEventListener('click', function(event) {
        if (!event.target.closest('.add-button')) {

            $.ajax({
                url: '/classes',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({  'action': 'view_desc', 'course_code': classCourse, 'course_name': className, 'global_netid': globalNetId    }),
                success: function(response) {
                    console.log(classCourse, className);
                    courseOverviewOverlay(classCourse, className);
                },
                error: function(error) {
                    console.log(error);
                }
            });
        };
    });

    return eachClass;
}

function addToPlan(courseCode, className) {
    const overlay = document.getElementById('add-to-plan-overlay-container');
    const content = document.getElementById('add-to-plan-overlay-content');
    const courseHeading = document.querySelector('.add-to-plan-course-heading');

    courseHeading.textContent = courseCode;

    overlay.style.display = 'block';

    const addButton = document.getElementById('add-to-plan-button');

    const addButtonClickHandler = function() {
        const yearDropdown = document.getElementById('add-course-year');
        const semesterDropdown = document.getElementById('add-course-semester');

        const year = yearDropdown.value;
        const semester = semesterDropdown.value;

        $.ajax({
            url: '/classes',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({  'action': 'add_to_plan', 'year': year, 'semester': semester, 'course': courseCode, 'class_name': className, 'global_netid': globalNetId   }),
            async: true,
            success: function(response) {
                window.location.reload();
                console.log('success');
            },
            error: function(error) {
                console.log(error);
            }
        });

        yearDropdown.selectedIndex = 0;
        semesterDropdown.selectedIndex = 0;

        overlay.style.display = 'none';
    };

    addButton.addEventListener('click', addButtonClickHandler);

    document.body.addEventListener('click', function(event) {
        if (event.target === overlay && !content.contains(event.target)) {
            overlay.style.display = "none";
            yearDropdown.selectedIndex = 0;
            semesterDropdown.selectedIndex = 0;
            addButton.removeEventListener('click', addButtonClickHandler);
        }
    });
}

function getEnrollmentsData() {
    $.ajax({
        url: '/getdata',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            showInPlan(data.unlt, "UNLT");
            showInPlan(data.frfa, "FRFA");
            showInPlan(data.frsp, "FRSP");
            showInPlan(data.sofa, "SOFA");
            showInPlan(data.sosp, "SOSP");
            showInPlan(data.jufa, "JUFA");
            showInPlan(data.jusp, "JUSP");
            showInPlan(data.sefa, "SEFA");
            showInPlan(data.sesp, "SESP");
            console.log('success');
        },
        error: function (error) {
            console.error('Error fetching enrollments:', error);
        }
    });
}

function showInPlan(enrollments, semester) {

    const planCardContainer = document.getElementById(semester);

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
        removeButton.addEventListener("click", function() {
            const semester = this.closest(".plan-card-courses").id;
            const courseCode = this.closest(".plan-card-single-course").querySelector(".plan-card-single-course-code").textContent;
            const courseName = this.closest(".plan-card-single-course").querySelector(".plan-card-single-course-name").textContent;

            courseDel(courseCode, courseName, semester);
        })
    
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
                    addToPlan(item[0], item[1]);
                });
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function onClassesPage() {
    return window.location.href.includes("classes");
}

function onLoginPage() {
    console.log("currently on: ", window.location.href);
    return window.location.href.includes("login");
}

function onRegisterPage() {
    return window.location.href.includes("register");
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        if (onClassesPage()) {
            searchClasses();
        } else if (onLoginPage()) {
            sendLoginData();
        } else if (onRegisterPage()) {
            sendRegisterData();
        }
    }
}

function courseDel(courseCode, courseName, semester) {

    const planCardContainer = document.getElementById(semester);

    const planCards = planCardContainer.getElementsByClassName("plan-card-single-course");
    for (const planCard of planCards) {
        const classCode = planCard.querySelector(".plan-card-single-course-code").textContent;
        const className = planCard.querySelector(".plan-card-single-course-name").textContent;

        if (classCode === courseCode && className === courseName) {
            planCard.remove();
            console.log("Found matching card");

            $.ajax({
                url: '/plan',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({  'global_netid': globalNetId, 'course_code': courseCode, 'semester': semester, 'course_name': courseName }),
                success: function(response) {
                    console.log(response.course_name, response.course_code, response.semester);
                },
                error: function(error) {
                    console.log('cannot delete');
                }
            })

            return;
        }
    }

    console.log("No plan card");
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

function courseOverviewOverlay(courseCode, courseName) {
    const overlay = document.getElementById('course-overview-overlay-container');
    const content = document.getElementById('course-overview-overlay-content');
    const courseCodeContent = document.getElementById('course-overview-course-code');
    const courseNameContent = document.getElementById('course-overview-course-name');

    courseCodeContent.textContent = courseCode;
    courseNameContent.textContent = courseName;

    overlay.style.display = 'block';

    document.body.addEventListener('click', function(event) {
        if (event.target === overlay && !content.contains(event.target)) {
            overlay.style.display = 'none';
        }
    });
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




