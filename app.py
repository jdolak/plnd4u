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
 
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)
