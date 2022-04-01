from app import app
from app.preprocess import preprocess
from flask import render_template
import gunicorn

stewards_data = preprocess()

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", stewards_data=stewards_data)

app.run(debug=True)