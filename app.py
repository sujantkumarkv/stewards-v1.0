from preprocess import preprocess
from flask import Flask, render_template
import gunicorn

app = Flask(__name__)

stewards_data = preprocess()

@app.route("/", methods=["GET", "POST"])
def index():
    #print(stewards_data)
    return render_template("index.html", stewards_data=stewards_data)

#@app.route("/json",  methods=["GET"])
#    return stewards_data

"""On removing below code, it doesn't run locally and removing it works for deployment. 
    We can infer from this that file's __name__ property, uses and how it's used in local development.
    But things change in deploying. `app.run` isn't needed. Infact, deploy didn't work Ig due to this."""
#if __name__ == "__main__":
#    app.run(debug=True)
app.run()