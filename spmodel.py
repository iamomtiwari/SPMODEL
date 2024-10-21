from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is your Flask app!"

if __name__ == "__main__":
    app.run(debug=True)
