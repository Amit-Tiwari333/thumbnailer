import os

from flask import Flask, flash, request, redirect, render_template, send_file
from io import BytesIO

from PIL import Image

SECRET_KEY = os.environ.get("SECRET_KEY", "notsosecret")
IMAGE_WIDTH = int(os.environ.get("IMAGE_WIDTH", "300"))
IMAGE_HEIGHT = int(os.environ.get("IMAGE_HEIGHT", "300"))

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def image_resize():
    if request.method == "POST":
        if not is_valid_file():
            flash("Invalid file!")
            return redirect(request.url)
        return resize_image()

    else:
        return render_template("index.html", width=IMAGE_WIDTH, height=IMAGE_HEIGHT)


def is_valid_file():
    if "file" not in request.files:
        return False
    f = get_file()
    if not f or not f.filename:
        return False
    return is_image(f.filename)


def get_file():
    return request.files["file"]


def is_image(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in [".jpg", ".jpeg"]


def resize_image():
    f = get_file()
    image = Image.open(BytesIO(f.read()))
    image.thumbnail((IMAGE_WIDTH, IMAGE_HEIGHT))
    buffer = BytesIO()
    image.save(buffer, "JPEG", quality=80)
    buffer.seek(0)
    return send_file(
        buffer, mimetype=f.mimetype, as_attachment=True, attachment_filename=f.filename
    )