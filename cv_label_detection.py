#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64encode
from os import makedirs
from os.path import join, basename
from sys import argv
import json
import requests

ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
API_KEY = 'AIzaSyAWoMVQkQxtjc6Vy0LCW8V6713YSlMdY4s'
RESULTS_DIR = 'jsons'
makedirs(RESULTS_DIR, exist_ok=True)

# リクエストの作成
def make_image_data_list(image_filenames):
    img_requests = []
    for imgname in image_filenames:
        with open(imgname, 'rb') as f:
            print(f)
            ctxt = b64encode(f.read()).decode()
            img_requests.append({
                    'image': {'content': ctxt},
                    'features': [{
                        'type': 'LABEL_DETECTION',
                        'maxResults': 5
                    }]
            })
    print(img_requests)
    return img_requests

# POST処理
def send_file_to_cloudvision(api_key, image_filenames):
    imgdict = make_image_data_list(image_filenames)
    response = requests.post(ENDPOINT_URL,
                            data=json.dumps({"requests": imgdict }).encode(),
                            params={'key': api_key},
                            headers={'Content-Type': 'application/json'})
    return response

if __name__ == '__main__':
    print("kick")
    api_key, *image_filenames = argv[1:]
    print(api_key)
    print(image_filenames)
#    *image_filenames = argv[2:]
    if not api_key or not image_filenames:
        print("""
	    適切にAPIキーとイメージファイルを指定してください。

        $ python cvapi.py api_key image.jpg""")
    else:
        response = send_file_to_cloudvision(api_key, image_filenames)
        if response.status_code != 200 or response.json().get('error'):
            print(response.text)
        else:
            # レスポンス表示
            for idx, resp in enumerate(response.json()['responses']):
                imgname = image_filenames[idx]
                jpath = join(RESULTS_DIR, basename(imgname) + '.json')
                print (json.dumps(resp, indent=2))
