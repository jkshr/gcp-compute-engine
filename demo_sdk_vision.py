import os
import io
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug import secure_filename
#from os import makedirs

from google.cloud import vision
from google.cloud.vision import types

# ファイル拡張子の許可リスト
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

#RESULTS_DIR = 'jsons'
#makedirs(RESULTS_DIR, exist_ok=True)

# 選択されたファイルの拡張子を確認
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':

        client = vision.ImageAnnotatorClient()

        file = request.files['file']
        if file and allowed_file(file.filename):
            image_filenames = request.files['file'].filename
            content = file.read()

            image = types.Image(content=content)

            response = client.label_detection(image=image)
            labels = response.label_annotations

#            print('Labels:')
#            print(labels)
#            for label in labels:
#                print(label.description)

            # 'labels'を直接返すと以下のエラーが出るためTBD
            # UnboundLocalError: local variable 'labels' referenced before assignment
            results = labels
    # index.htmlに結果を返す
    return render_template('index.html', type='label detection', results=results)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
