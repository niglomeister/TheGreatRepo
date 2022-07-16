import time
from subprocess import run, Popen
import os

from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)
Popen(["lbrynet", "start"]) #start the lbry node

@app.route("/")
def index():
    vid_title = "An introduction to PepeVision"
    return render_template("index.html", vid_title=vid_title)

@app.route("/vid")
def vid():
    return redirect("/")

@app.route("/results", methods = ["POST","GET"])
def results():
    query = request.args.get("query")
    if query:
        res = run(["lbrynet","resolve",query], capture_output = True)
    else:
        res = run(["lbrynet","resolve",""], capture_output = True)
    print("=======================","\n",res.stdout)
    return res.stdout, 200, {"content-Type": "text/plain"}

@app.route("/direct_search")
def direct_search():
    query = request.args.get("query")
    res = run(["lbrynet","resolve",query], capture_output = True)
    print(type(res.stdout))

    return res.stdout

if __name__ == "__main__":
    app.run(debug=True)