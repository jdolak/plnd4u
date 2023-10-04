from flask import Flask, render_template, request, session

# instance of flask application
app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template('index.html')
@app.route("/devplan")
def devplan():
    return render_template('devplan.html')
 
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)
