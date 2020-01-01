from flask import Flask, jsonify, render_template, request, url_for, Response
from bson.json_util import dumps
from collections import Counter
from bson import ObjectId

from pyquery import PyQuery as pq
import pymongo
import json
import requests
from wordcloud import WordCloud
import pandas as pd
import matplotlib

app = Flask(__name__,  template_folder="templates")

URI = "mongodb://db:27017/"
news_client = pymongo.MongoClient(URI)
if "news_database" in news_client.list_database_names():
    news_client.drop_database("news_database")
news_database = news_client["news_database"]
news = news_database["news"]

@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        r = requests.get("http://scraper:5000/")
        return render_template("index.html")

"""@app.route("/graph", methods=["GET"])
def graph():
    if request.method == "GET":
        return render_template("lda.html")"""

@app.route("/results", methods=["GET"])
def resultados():
    if request.method == "GET":
        r = requests.get("http://backend:5000/results")
        return render_template("results.html", ldap = r.json())

@app.route("/nube", methods=["GET"])
def nube():
    if request.method == "GET":
        r = requests.get("http://backend:5000/lista")
        wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
        wordcloud.generate(r.text)
        y = wordcloud.to_image()
        return render_template("recommendations.html", y = y)

@app.route("/recommendations", methods=["GET"])
def recommends():
    if request.method == "GET":
        r = requests.get("http://backend:5000/recommendations")
        return render_template("recommendations.html")


@app.route("/resrec", methods=["POST"])
def prediction():
    form = request.form
    if request.method == "POST":

        topic = -1
        topic0 = request.form['Topic0']
        topic1 = request.form['Topic1']
        topic2 = request.form['Topic2']
        topic3 = request.form['Topic3']
        topic4 = request.form['Topic4']
        if topic0 is not None:
            topic = 0
        elif topic1 is not None:
            topic = 1
        elif topic2 is not None:
            topic = 2
        elif topic3 is not None:
            topic = 3
        elif topic4 is not None:
            topic = 4
        r = requests.post("http://backend:5000/resrec", data = json.dumps({"msg":topic}))
        return render_template("resrec.html")
