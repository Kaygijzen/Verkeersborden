import os
from flask import Flask, redirect, url_for, render_template, request, send_file
from werkzeug.utils import secure_filename
import csv
import shutil

from model import predict_images

app = Flask(__name__, static_url_path='/static')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
FOLDER = './static/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def route():
    return redirect(url_for('index'))


@app.route('/index/')
def index():
    files = os.listdir('./static/')
    return render_template('index.html', files=files)


@app.route('/upload/', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file[]")
    for file in uploaded_files:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(FOLDER + filename)
    return redirect(url_for('index'))


@app.route('/clear/', methods=['POST'])
def clear():
    for filename in os.listdir(FOLDER):
        file_path = os.path.join(FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return redirect(url_for('index'))


@app.route("/result/")
def result():
    predictions = predict_images(FOLDER)
    with open('predictions.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for prediction in predictions:
            writer.writerow(prediction)
    return render_template('result.html', predictions=predictions)


@app.route('/download/', methods=['POST'])
def download_file():
    return send_file("predictions.csv", as_attachment=True)


if __name__ == "__main__":
    app.run()
