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
            url: '/plan',
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

function searchClasses() {
    const searchInput = document.getElementById('search-bar').value;
    $.ajax({ 
        url: '/classes',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({  'action': 'search', 'search_input': searchInput }),
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
