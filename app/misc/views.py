from flask import render_template, request, redirect

from app import app

@app.route('/')
def home():
    if 'Bright' in request.headers.get('User-Agent'):
        return redirect('/booth')
    return render_template('home.html')

# do something to explicitly handle HTTP errors so we don't get some general nginx page

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404

@app.errorhandler(405)
def page_not_found(e):
    return "you're no good, you're no good"

@app.errorhandler(500)
def handle_exception(e):
    return render_template("broken.html", e=e), 500