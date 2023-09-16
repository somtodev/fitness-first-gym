from flask import render_template, session, redirect
from app import app


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template("pages/error/404.html")


@app.errorhandler(500)
def server_error(e):
    print(e)
    return render_template("pages/error/500.html")