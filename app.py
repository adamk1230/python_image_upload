import os
from os.path import join, dirname, realpath
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/UPLOAD_FOLDER'
UPLOADS_PATH = join(dirname(realpath(__file__)), UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

image_object = None

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #building the url for the img src
            uploads_url = url_for('uploaded_file',filename=filename)
            uploads_url = uploads_url[1:]

            img_src = request.url + uploads_url

            #building the object for Jinja
            global image_object
            image_object = {"path": img_src}

            return redirect(url_for('uploaded_file',filename=filename))
    return render_template("index.html", image = image_object)


#route to send image to browser
@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)


