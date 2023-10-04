from flask import Flask

# instance of flask application
app = Flask(__name__)
 
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
def index():
    return render_template('index.html')
 
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)
