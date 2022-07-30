import time
from subprocess import run, Popen
import os
from urllib.request import urlopen
from urllib.parse import quote_plus
import json
import asyncio
import requests
from math import ceil

from flask import Flask, render_template, url_for, redirect, request
from flask_socketio import SocketIO
import flask

from utils import safeget, reorder_results

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!!!-'
socketio = SocketIO(app)

Popen(["lbrynet", "start","--quiet"]) #start the lbry node

@app.route("/")
def index():
    vid_title = "An introduction to PepeVision"
    return render_template("index.html", vid_title=vid_title)

@app.route("/direct_search")
def direct_search():
    query = request.args.get("query")
    res = run(["lbrynet","get",query], capture_output = True)
    return res.stdout


@app.route("/results", methods = ["POST","GET"])
async def results():
    query = request.args.get("query")
    search_response = urlopen(f'https://lighthouse.lbry.com/search?s={quote_plus(query)}').read()  
    search_results = json.loads(search_response)

    return render_template("results.html",search_results = search_results)


@app.route("/api/results_thumbnails", methods = ["POST"])
def results_thumbnails():
    claim_ids = [claim["claimId"] for claim in request.json ]

    res = requests.post("http://localhost:5279", json={"method": "claim_search", "params": {"claim_ids": claim_ids }}).json()["result"]["items"]
    res = reorder_results(querys = claim_ids, results = res)

    thumbnail_urls, titles, claim_types, descriptions, channels = [], [], [], [], []
    for r in res:
        thumbnail_urls.append(safeget(r,['value','thumbnail','url'], placeholder = sad_pepe ))
        titles.append(safeget(r,['value','title']))
        claim_types.append(r["value_type"])
        descriptions.append(safeget(r,["value","description"],placeholder = ''))
        channels.append(safeget(r,["signing_channel"],'no channel'))
    print(channels)
    url_and_titles = {'urls':thumbnail_urls, 'titles':titles, "type":claim_types, "descriptions": descriptions, "channels":channels}
    return url_and_titles

sad_pepe = 'https://avatars.mds.yandex.net/i?id=c7512b5b2de6ff3577c33ddc60afc846-4569389-images-thumbs&n=13&exp=1'

@app.route("/stream/<url>")
def stream(url):
    res = requests.post("http://localhost:5279", json={"method": "get", "params": {"uri": url }}).json()["result"]

    if res.get("error") == "Invalid LBRY stream URL: '@Fff'":
        claim_type = requests.post("http://localhost:5279", json={"method": "resolve", "params": {"urls": url }}).json()["result"][url]["value_type"]
        return redirect(f"/{claim_type}/{url}")

    return render_template("/stream.html", id=id, meta=res.get("metadata",None) , streaming_url = res.get("streaming_url"), 
            description = safeget(res,["metadata","description"],''), stream_title = res["metadata"]["title"], claim = res)

@app.route("/channel/<url>/")
@app.route("/channel/<url>/<int:page>")
def channel(url,page = 1):
    page_size = 20

    res = requests.post("http://localhost:5279", json={"method": "claim_search", "params": {"channel": url, "no_totals": True, "page": page }}).json()["result"]
    claims = res["items"]

    if not claims:
        channel = requests.post("http://localhost:5279", json={"method": "resolve", "params": {"urls": url}}).json()["result"][url]
        n_claims = n_pages = 0
        channel_name = safeget(channel,['value','title'],placeholder=channel['name'])
        channel_thumbnail = sad_pepe
    
    else :
        channel = claims[0]["signing_channel"]
        n_claims = channel["meta"]["claims_in_channel"]
        n_pages = ceil(n_claims/page_size)
        channel_name = safeget(channel,["value","title"],'')
        channel_thumbnail = channel["value"]["thumbnail"]["url"]

    return render_template("channel.html",claims = claims, n_pages = n_pages, current_page = page, url = url, channel_name = channel_name,
     channel_thumbnail = channel_thumbnail, channel = channel)

@app.route("/collection/<url>/<int:page>")
@app.route("/collection/<url>")
def collection(url, page = 1):
    collection = requests.post("http://localhost:5279", json={"method": "resolve",
     "params": {"urls":url}}).json()["result"][url]
    claim_ids = collection["value"]["claims"]
    title = collection["value"]["title"] 
    thumbnail = collection["value"]["thumbnail"]["url"]

    claims = requests.post("http://localhost:5279", json={"method": "claim_search",
     "params": {"claim_ids": claim_ids, "no_totals": True, "page": page }}).json()["result"]["items"]

    return render_template("/collection.html", claims=claims, title=title, thumbnail = thumbnail)

if __name__ == "__main__":
    app.run(debug=True)