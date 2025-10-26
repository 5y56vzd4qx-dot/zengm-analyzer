from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import json, gzip, os
from utils.parser import parse_zengm

app = Flask(__name__, template_folder="templates", static_folder="static")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            data = parse_zengm(path)
            data["overview"].to_csv("uploads/overview.csv", index=False)
            data["teams"].to_csv("uploads/teams.csv", index=False)
            data["players"].to_csv("uploads/players.csv", index=False)
            data["stats"].to_csv("uploads/stats.csv", index=False)
            return redirect(url_for("overview"))
    return render_template("index.html")

@app.route("/overview")
def overview():
    df = pd.read_csv("uploads/overview.csv")
    return render_template("overview.html", tables=[df.to_html(classes="table table-striped", index=False)])

@app.route("/teams")
def teams():
    df = pd.read_csv("uploads/teams.csv")
    return render_template("teams.html", tables=[df.to_html(classes="table table-hover", index=False)])

@app.route("/players")
def players():
    df = pd.read_csv("uploads/players.csv")
    return render_template("players.html", tables=[df.to_html(classes="table table-hover", index=False)])

@app.route("/stats")
def stats():
    df = pd.read_csv("uploads/stats.csv")
    return render_template("stats.html", tables=[df.to_html(classes="table table-hover", index=False)])

@app.route("/records")
def records():
    df = pd.read_csv("uploads/stats.csv")
    leaders = {
        "Most Goals": df["G"].max() if "G" in df.columns else "N/A",
        "Most Assists": df["A"].max() if "A" in df.columns else "N/A",
        "Most Points": df["PTS"].max() if "PTS" in df.columns else "N/A"
    }
    return render_template("records.html", leaders=leaders)

if __name__ == "__main__":
    app.run(debug=True)
