from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars_data_d = mongo.db.mars_data_d.find_one()
    return render_template("index.html", mars_data_d=mars_data_d)
 
@app.route("/scrape")
def scrape():
    mars_data_d = mongo.db.mars_data_d
    mars_data = scrape_mars.scrape_all()
    mars_data_d.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run()