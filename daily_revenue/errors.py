from app import app
from flask import render_template

@app.errorhandler(404)
def page404(error):
    return render_template('page404.html'), 404


@app.errorhandler(500)
def page500(error):
    return render_template('page500.html'), 500