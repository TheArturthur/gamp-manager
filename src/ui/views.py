from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("base.html")

@views.route('/new-project')
def new_project():
    return render_template("new_project.html", name="Proyecto Prueba")