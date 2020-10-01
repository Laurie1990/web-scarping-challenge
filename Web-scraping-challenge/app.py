from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/marsinfo")

@app.route("/")
def index():
    marsinfo = mongo.db.marsinfo.find_one()
    return render_template("index.html", marsinfo=marsinfo)

@app.route("/scrape")
def scraper():
    marsinfo = mongo.db.marsinfo
    marsdata = scrape_mars.scrape()
    marsinfo.update(
        {},
        marsdata, 
        upsert=True
    )
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)