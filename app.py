from preprocess import preprocess
from flask import Flask, render_template
import gunicorn

app = Flask(__name__)

stewards_data = preprocess()

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", stewards_data=stewards_data)

app.run(debug=True)