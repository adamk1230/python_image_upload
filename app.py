import os
import io
from os.path import join, dirname, realpath
from flask import Flask, render_template, redirect, url_for, request, send_from_directory, send_file
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/UPLOAD_FOLDER'
UPLOADS_PATH = join(dirname(realpath(__file__)), UPLOAD_FOLDER)
#extension validation
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#set global variable to be used in upload_file() and uploaded_file()
stream_file = None

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
            #call the global variable
            global stream_file
            #set stream_file as a BytesIO Object
            stream_file = io.BytesIO()
            #save the request file to stream_file
            file.save(stream_file)
            #set the objects position to the beginning of the file
            stream_file.seek(0)


            return redirect(url_for('uploaded_file'))
    return render_template("index.html")


#route to send image to browser
@app.route('/uploads')
def uploaded_file():

    #use the send_file helper to send the image back to the browser
    return send_file(stream_file, attachment_filename="img.jpeg")


if __name__ == "__main__":
    app.run(debug=True)


