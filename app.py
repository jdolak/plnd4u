from flask import Flask, render_template, request, url_for, jsonify
import sys

sys.path.append('/plnd4u/src')
from func_basic import *

# instance of flask application
app = Flask(__name__)
 
@app.route("/")
@app.route("/home")
def home():
    css_url = url_for('static', filename='css/styles.css')
    return render_template('home.html', css_url=css_url)
 
@app.route("/register")
def register():
    css_url = url_for('static', filename='css/styles.css')
    return render_template('register.html', css_url=css_url)

@app.route("/classes", methods=['POST', 'GET'])
def classes():
    if request.method == 'POST':
        data = request.get_json()
        course_name = data.get('course_name')
        course_code = data.get('course_code')
        search_input = data.get('search_input')
        db_enroll_class("XXX",course_code, "FA00")
        search_output = db_search_past_classes(search_input)

        return jsonify(course_name=course_name, course_code=course_code, search_output=search_output)
    css_url = url_for('static', filename='css/styles.css')
    js_url = url_for('static', filename='js/script.js')
    return render_template('classes.html', css_url=css_url, js_url=js_url)

@app.route("/plan", methods=['POST', 'GET'])
def plan():
    if request.method == 'POST':

        data = request.get_json()
        course_year = data.get('year')
        course_semester = data.get('semester')
        course_code = data.get('course')
        db_del_all_enrollments("XXX")
        LOG.debug("u have sent a post to plan")

        return jsonify(course_year=course_year, course_semester=course_semester, course_code=course_code)

    enrollments = db_show_student_enrollments("XXX")
    msg = ""
    for i in enrollments:
        msg = f"{msg}{i[0]} {i[1]}, "
    enrollments = msg
    css_url = url_for('static', filename='css/styles.css')
    js_url = url_for('static', filename='js/script.js')
    return render_template('plan.html', css_url=css_url, js_url=js_url, enrollments=enrollments)

    

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        netid = data.get('netid')
        db_register_student(netid,"XXXX", "XXX", "0000")
        return jsonify(netid=netid)
    css_url = url_for('static', filename='css/styles.css')
    js_url = url_for('static', filename='js/script.js')
    return render_template('login.html', css_url=css_url, js_url=js_url)

@app.route("/devplan")
def devplan():
    return render_template('devplan.html')

@app.route("/about")
def about():
    css_url = url_for('static', filename='css/styles.css')
    js_url = url_for('static', filename='js/script.js')
    return render_template('about.html', css_url=css_url, js_url=js_url)
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)
