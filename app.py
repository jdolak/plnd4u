from flask import Flask, render_template, request, url_for, jsonify, session, redirect
import sys
import time

sys.path.append("/plnd4u/src")
from func_adv import *

app = Flask(__name__)
app.secret_key = str(time.time())


@app.route("/")
@app.route("/home")
def home():
    css_url = url_for("static", filename="css/styles.css")
    return render_template("home.html", css_url=css_url)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        data = request.get_json()
        netid = data.get("netid")
        session["netid"] = netid

        status = register_student(
            netid,
            f"{data.get('first_name')} {data.get('last_name')}",
            data.get("major"),
            data.get("grad"),
            data.get("pw"),
        )

        return jsonify(netid=netid, status=status)

    css_url = url_for("static", filename="css/styles.css")
    js_url = url_for("static", filename="js/script.js")

    return render_template("register.html", css_url=css_url, js_url=js_url)


@app.route("/classes", methods=["POST", "GET"])
def classes():
    if "netid" not in session:
        LOG.info("redirecting to login...")
        return redirect(url_for("login"))

    netid = session["netid"]

    if request.method == "POST":
        data = request.get_json()
        action = data.get("action")

        match action:
            case "add":
                course_name = data.get("course_name")
                course_code = data.get("course_code")

                db_enroll_class(netid, course_code, "UNLT", course_name)
                return jsonify(course_name=course_name, course_code=course_code)

            case "add_to_plan":
                course_year = data.get("year")
                course_semester = data.get("semester")
                course_code = data.get("course")
                class_name = data.get("class_name")

                sem = f"{course_year[0:2].upper()}{course_semester[0:2].upper()}"

                if sem == "NONO":
                    return jsonify(
                        course_year=course_year,
                        course_semester=course_semester,
                        course_code=course_code,
                    )

                db_enroll_class(netid, course_code, sem, class_name)

                return jsonify(
                    course_year=course_year,
                    course_semester=course_semester,
                    course_code=course_code,
                )

            case "search":
                search_input = data.get("search_input")
                filter_input = data.get("filter_data")

                fall_semester = filter_input.get("fall-semester")
                spring_semester = filter_input.get("spring-semester")
                level_one = filter_input.get("10000")
                level_two = filter_input.get("20000")
                level_three = filter_input.get("30000")
                level_four = filter_input.get("40000")
                uni_req = filter_input.get("uni-req")
                major_req = filter_input.get("major-req")
                major_elective = filter_input.get("major-elective")

                filters = (
                    fall_semester,
                    spring_semester,
                    level_one,
                    level_two,
                    level_three,
                    level_four,
                    uni_req,
                    major_req,
                    major_elective,
                )

                search_output = db_search_past_classes(netid, search_input, filters)
                return jsonify(search_output=search_output)

            case "view_desc":
                course_code = data.get("course_code")
                course_name = data.get("course_name")

                desc = db_show_description(course_code)
                credits = db_show_credits(course_code)
                core_reqs = db_show_core_reqs(course_code)
                recent_sems = db_show_semesters(course_code)
                profs = db_show_profs(course_code)
                meeting_times = db_show_meeting_times(course_code)
                coreqs = db_show_coreqs(course_code)
                prereqs = db_show_prereqs(course_code)

                return jsonify(
                    desc=desc,
                    credits=credits,
                    core_reqs=core_reqs,
                    recent_sems=recent_sems,
                    profs=profs,
                    meeting_times=meeting_times,
                    coreqs=coreqs,
                    prereqs=prereqs,
                )

    css_url = url_for("static", filename="css/styles.css")
    js_url = url_for("static", filename="js/script.js")

    return render_template("classes.html", css_url=css_url, js_url=js_url)


@app.route("/getdata", methods=["GET"])
def getdata():
    if "netid" not in session:
        LOG.info("redirecting to login...")
        return redirect(url_for("login"))

    netid = session["netid"]

    if request.method == "GET":

        unlt = db_show_student_enrollments_short(netid, "UNLT")
        frfa = db_show_student_enrollments_short(netid, "FRFA")
        frsp = db_show_student_enrollments_short(netid, "FRSP")
        sofa = db_show_student_enrollments_short(netid, "SOFA")
        sosp = db_show_student_enrollments_short(netid, "SOSP")
        jufa = db_show_student_enrollments_short(netid, "JUFA")
        jusp = db_show_student_enrollments_short(netid, "JUSP")
        sefa = db_show_student_enrollments_short(netid, "SEFA")
        sesp = db_show_student_enrollments_short(netid, "SESP")

        credit = db_show_sem_credits_all(netid)

        missing_prerequisites = db_check_prerequisites(netid)
        missing_corequisites = db_check_corequisites(netid)

        return jsonify(
            unlt=unlt,
            frfa=frfa,
            frsp=frsp,
            sofa=sofa,
            sosp=sosp,
            jufa=jufa,
            jusp=jusp,
            sefa=sefa,
            sesp=sesp,
            unlt_credit=credit[0],
            frfa_credit=credit[1],
            frsp_credit=credit[2],
            sofa_credit=credit[3],
            sosp_credit=credit[4],
            jufa_credit=credit[5],
            jusp_credit=credit[6],
            sefa_credit=credit[7],
            sesp_credit=credit[8],
            missing_prerequisites=missing_prerequisites,
            missing_corequisites=missing_corequisites,
        )


@app.route("/plan", methods=["POST", "GET"])
def plan():
    if "netid" not in session:
        LOG.info("redirecting to login...")
        return redirect(url_for("login"))

    netid = session["netid"]
    enrollments = db_show_student_enrollments(netid, 0)

    if request.method == "POST":
        data = request.get_json()
        action = data.get("action")

        if action == "delete":
            course_code = data.get("course_code")
            course_name = data.get("course_name")
            semester = data.get("semester")

            db_del_enrollment(netid, course_code, semester, course_name)

            return jsonify(
                course_code=course_code, course_name=course_name, semester=semester
            )

        elif action == "missing_reqs":
            core_requirements = db_check_core_requirements(netid)
            required_courses = db_check_required_courses(netid)
            electives = db_check_electives(netid)

            return jsonify(
                core_requirements=core_requirements, required_courses=required_courses, electives=electives
            )

    css_url = url_for("static", filename="css/styles.css")
    js_url = url_for("static", filename="js/script.js")

    return render_template(
        "plan.html", css_url=css_url, js_url=js_url, enrollments=enrollments
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        data = request.get_json()
        netid = data.get("netid")

        status = db_check_login(netid, data.get("pw"))
        if not status:
            session["netid"] = netid

        return jsonify(netid=netid, status=status)

    css_url = url_for("static", filename="css/styles.css")
    js_url = url_for("static", filename="js/script.js")

    return render_template("login.html", css_url=css_url, js_url=js_url)


@app.route("/devplan")
def devplan():
    return render_template("devplan.html")


@app.route("/about")
def about():
    css_url = url_for("static", filename="css/styles.css")
    js_url = url_for("static", filename="js/script.js")

    return render_template("about.html", css_url=css_url, js_url=js_url)


if __name__ == "__main__":
    if DEPLOY_ENV == "prod":
        from waitress import serve

        serve(app, host="0.0.0.0", port=80)
    else:
        app.run(debug=True, host="0.0.0.0", port=80)

# pyright: reportMissingModuleSource=false
# pyright: reportMissingImports=false
