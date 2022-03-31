from app import app
from app.preprocess import preprocess
from flask import render_template

stewards_data = preprocess()

@app.route("/", methods=["GET", "POST"])
def index():
    #proposals_data = get_proposals()
    #proposal_number = len(proposals_data)
    #print(number_prop.number)
    #if proposal_number != number_prop.number:
    #    initial_list, number_prop = preprocess()
    

    return render_template("index.html", stewards_data=stewards_data)
