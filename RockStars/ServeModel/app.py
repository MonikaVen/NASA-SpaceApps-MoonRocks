from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import tensorflow as tf

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/model'

# # Load your trained model
#model = load_model(MODEL_PATH)
model = tf.keras.models.load_model(MODEL_PATH)
#model._make_predict_function()          # Necessary

print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
# from keras.applications.inception_v3 import InceptionV3
# model = InceptionV3()
# print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(256, 256))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)
    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    # x = preprocess_input(x, mode='caffe')
    preds = model.predict_generator(x)
    # preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        
        # Make prediction
        preds = model_predict(file_path, model)

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        # pred_class = decode_predictions(preds, top=3)   # ImageNet Decode
        # result = str(pred_class[0][0][1])               # Convert to string
        formatted_res = []
        for pred in preds[0]:
            res = ''
            if pred >= 0.6:
                res = "<div class='sure'>" + str(round(pred*100, 2)) 
            else:
                res = "<div class='unsure'>" + str(round(pred*100, 2)) 
            formatted_res.append(res)



        result = formatted_res[0] + '%  Anorthite <br>' + "</div>" + formatted_res[1] + '%  Basalt <br>' + "</div>"+ formatted_res[2] + '%  Breccia <br>' + "</div>"
        
        
        if round(max(preds[0])) < 0.5:
            message = 'High uncertainty! <br> Collect the sample.'
            collect = True
        elif round(max(preds[0])) > 0.6:
            message = 'Known rock!'
            collect = False
        # else:
        #     message = 'Scan again!'
        #     collect = False
        return {'message': message, 'result' : result, 'collect' : collect}
    return None


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
