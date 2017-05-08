# -*- coding: utf-8 -*-
import os
import sys
tastemaker = os.path.dirname(os.getcwd())
sys.path.append(tastemaker)
from image_to_category import image_to_category

from flask import Flask, render_template, send_file, request, abort, redirect
app = Flask(__name__, template_folder='.')

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/infer', methods=['POST'])
def infer():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'pic' not in request.files:
            return "Request does not contain file", 400
        file = request.files['pic']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "Empty filename", 400
        if file:
            file.save(os.path.join('upload.jpg'))
#            answer = run_inference_on_image()
            predicted_categories, top5_labels, top5_proba = image_to_category('upload.jpg')
            print(answer)
            return answer, 200


@app.route('/main.js')
def js():
    return send_file('main.js')


if __name__ == '__main__':
    app.run()