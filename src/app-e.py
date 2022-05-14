from flask import Flask, render_template, request, url_for, redirect
from flask_migrate import Migrate

from src import routes, utils as u
from src.models import db
from src.settings import Settings as S
from src.tasks import make_celery
import io


file_text = "def __init__(): self.number = 1"
app= Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template("base.html", file_text = "i == 1 or i%2 == 1")

@app.route("/process", methods=["POST"])
def process_code():
    file_text = get_text()
    return redirect(url_for("index"))

def get_text():
    return request.form["codeinput"]

if __name__ == "__main__":
	app.run(debug=True)
