import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from base64 import b64encode
from os import makedirs
from os.path import join, basename
from sys import argv
import json
import requests

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
API_KEY = 'AIzaSyAWoMVQkQxtjc6Vy0LCW8V6713YSlMdY4s'

app = Flask(__name__)

#RESULTS_DIR = 'jsons'
#makedirs(RESULTS_DIR, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        image_filenames = request.files['file'].filename
        print(image_filenames)
        ctxt = b64encode(file.read()).decode()
#        ctxt = b64encode(request.files['file'].read()).decode()
#        print(ctxt.decode())

        img_requests = []
        img_requests.append({
            'image': {'content': ctxt},
            'features': [{
            'type': 'LABEL_DETECTION',
            'maxResults': 5
            }]
        })
#        print(img_requests)

        response = requests.post(ENDPOINT_URL,
            data=json.dumps({"requests": img_requests }).encode(),
            params={'key': API_KEY},
            headers={'Content-Type': 'application/json'})

        # レスポンス表示
        if response.status_code != 200 or response.json().get('error'):
            print(response.text)
        else:
            for idx, resp in enumerate(response.json()['responses']):
                imgname = image_filenames[idx]
                jpath = join(RESULTS_DIR, basename(imgname) + '.json')
                print (json.dumps(resp, indent=2))


#            response = send_file_to_cloudvision(file)
#            if response.status_code != 200 or response.json().get('error'):
#                print(response.text)
#            else:
#                # レスポンス表示
#                for idx, resp in enumerate(response.json()['responses']):
#                    imgname = image_filenames[idx]
#                    jpath = join(RESULTS_DIR, basename(imgname) + '.json')
#                    print (json.dumps(resp, indent=2))
#            return redirect(url_for('uploaded_file', filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
