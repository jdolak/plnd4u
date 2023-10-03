from flask import Flask

# instance of flask application
app = Flask(__name__)
 
# home route that returns below text
# when root url is accessed
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
 
if __name__ == '__main__':
    app.run(debug=True, port=8080)
