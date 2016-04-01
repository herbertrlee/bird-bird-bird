from flask import Flask, request, render_template, url_for
from vison_utils import is_it_a_bird

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/', methods=["GET", "POST"])
def root():
    """Return a friendly HTTP greeting."""
    if request.method == "GET":
        return render_template("index.html")
    else:
        image_file = request.files["bird_image"]
        image_bytes = image_file.read()

        is_bird = is_it_a_bird(image_bytes)

        if is_bird:
            return render_template("index.html", bird=True)
        else:
            return render_template("index.html", bird=False)


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
