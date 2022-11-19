import numpy as np
from flask import Flask, request, render_template, jsonify
import pickle

import requests
import json

API_KEY = "XMGyyPuQidd9AY75a3we-PvLGeJ8Wyck7wmts7XiJVK4"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                     API_KEY,
                                                                                 "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/submit", methods=["POST"])
def prediction():
    if request.method == "POST":
        cyl = request.form["cylinder"]
        dis = request.form["displacement"]
        hp = request.form["horsepower"]
        w = request.form["weight"]
        a = request.form["a"]
        my = request.form["my"]
        ori = request.form["ori"]
        total = [[int(cyl), int(dis), int(hp), int(w), int(a), int(my), int(ori)]]

        payload_scoring = {"input_data": [{"field": [["cylinder", "displacement", "horsepower",
                                                      "weight", "a", "my", "ori"]],
                                           "values": total}]}
        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e4882d87-eacf-4877-846a-c170a77ca63d/predictions?version=2022-11-18',
            json=payload_scoring,
            headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        predictions = response_scoring.json()
        pre = predictions['predictions'][0]['values'][0][0]
        if (pre > 15):
            print("It is in a good condition")
        else:
            print("Not in a good condition")

        p = model.predict(total)
        return render_template("result.html", p=round(p[0], 2))

if __name__ == "__main__":
    app.run(debug=True)