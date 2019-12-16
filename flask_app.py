import os
import time

from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS, cross_origin
from detectWeb import inference
import torch


UPLOAD_FOLDER = 'WEB_DATA/in/'

app = Flask(__name__)
CORS(app)

if not(os.path.exists(UPLOAD_FOLDER)):
        os.mkdir(UPLOAD_FOLDER)
out = ''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global out
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        if not os.path.isfile(os.path.join('WEB_DATA/out/', filename)):

            if not os.path.isfile(os.path.join(UPLOAD_FOLDER, filename)):
                print("saving.....")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            else: print('already saved')

            with torch.no_grad():
                print('predicting.....')
                out = inference(os.path.join(UPLOAD_FOLDER, filename))

        return send_file(os.path.join('WEB_DATA/out/', filename), as_attachment=True)

@app.route('/direction',methods=['GET'])
def get_dir():
    global out
    return jsonify(out)



if __name__ == '__main__':
    app.run(port=8080)
