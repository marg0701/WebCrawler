from flask import Flask, jsonify, render_template, request, url_for
from bson.json_util import dumps
from collections import Counter
from OurScrapping import UpdateNews

from pyquery import PyQuery as pq
import pandas as pd
from pymongo import MongoClient
import json
import OurScrapping
import os

app = Flask(__name__)

Elpais_url = "https://elpais.com/internacional/"
Excelsior_url = "https://www.excelsior.com.mx/global#view-1"
CNN_url = "https://cnnespanol.cnn.com/seccion/mundo/"

news_client = MongoClient("mongodb://db:27017/")
if "news_database" in news_client.list_database_names():
    news_client.drop_database("news_database")
news_database = news_client["news_database"]
news = news_database["news"]

@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        df_1, df_2, df_3 = UpdateNews(Elpais_url,Excelsior_url,CNN_url)
        df = pd.concat([df_1, df_2, df_3])
        dict1 = df.to_dict(orient='records')
        x = news.insert_many(dict1)

