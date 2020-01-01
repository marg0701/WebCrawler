from flask import Flask, jsonify, render_template, request, url_for, Response
from bson.json_util import dumps
from collections import Counter

from pyquery import PyQuery as pq
import pandas as pd
import numpy as np
import pymongo
import json
from model import lda, show_docs, word_cloud


app = Flask(__name__, static_url_path='', static_folder='')

URI = "mongodb://db:27017/"
news_client = pymongo.MongoClient(URI)
news_database = news_client["news_database"]
news = news_database["news"]

"""@app.route("/results", methods=["GET"])
def resultados():
    if request.method == "GET":
        df_news = pd.DataFrame(json.loads(dumps(news.find({}))))
        vis = lda(df_news)
        return vis"""

@app.route("/lda", methods=["GET"])
def graph():
    if request.method == "GET":
        return render_template("lda.html")

@app.route("/lista", methods=["GET"])
def lista():
    if request.method == "GET":
        return 'Leche queso pan huevos cereal'

"""@app.route("/recommendations", methods=["GET"])
def recommends():
    if request.method == "GET":
        return ({"Hola":"Recomendaciones"})"""

@app.route("/resrec", methods=["GET","POST"])
def prediction():
    if request.method == "POST":
        df_news = pd.DataFrame(json.loads(dumps(news.find({}))))
        df = show_docs(df_news)
        df
        x = [ObjectId(r["$oid"]) for r in rec]
        presave = json.loads(dumps(news.find({"_id": {"$in": x}},{'Title':1,'URL':1})))
        return presave
