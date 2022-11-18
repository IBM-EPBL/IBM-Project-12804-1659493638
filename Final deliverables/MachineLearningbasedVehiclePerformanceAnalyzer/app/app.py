import numpy as np
from flask import Flask, request, render_template, jsonify
import pickle

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

        p = model.predict(total)
        return render_template("result.html", p=round(p[0], 2))

if __name__ == "__main__":
    app.run(debug=True)