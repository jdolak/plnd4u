from flask import Flask, render_template, request, session, url_for

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

@app.route("/classes")
def classes():
    css_url = url_for('static', filename='css/styles.css')
    js_url = url_for('static', filename='js/script.js')
    return render_template('classes.html', css_url=css_url, js_url=js_url)


@app.route("/plan")
def plan():
    css_url = url_for('static', filename='css/styles.css')
    return render_template('plan.html', css_url=css_url)

@app.route("/login")
def login():
    css_url = url_for('static', filename='css/styles.css')
    return render_template('login.html', css_url=css_url)

@app.route("/devplan")
def devplan():
    return render_template('devplan.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)
