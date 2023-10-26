from flask import Flask, render_template, request, url_for, jsonify
import sys
sys.path.append('/plnd4u/src')
from func_basic import *

import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# instance of flask application
app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template('index.html')

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
        return jsonify(course_name=course_name, course_code=course_code)
    css_url = url_for('static', filename='css/styles.css')
    js_url = url_for('static', filename='js/script.js')
    return render_template('classes.html', css_url=css_url, js_url=js_url)

@app.route('/plan')
def plan():
    css_url = url_for('static', filename='css/styles.css')
    js_url = url_for('static', filename='js/script.js')
    return render_template('plan.html', css_url=css_url, js_url=js_url)

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

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)
