from flask import Flask, jsonify, request
import base64
import json
import numpy as np
import cv2
import easyocr
import os
import sys
sys.path.append(os.getcwd())
from ocr_inf_utils import *

app = Flask(__name__)

# load inference model
reader = easyocr.Reader(['ko'], recog_network ='best_accuracy',
                        user_network_directory='custom_models/user_network',
                        model_storage_directory="custom_models/models")

# load fix_dict
with open("dia4_fix_db.json", "r") as f:
    fix_dict_lst = json.load(f)

@app.route('/ocr', methods=['POST'])
def ocr():
    data_dict = json.loads(request.data)
    img_string = data_dict['image']
    jpg_original = base64.b64decode(img_string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    cv_img = cv2.imdecode(jpg_as_np, flags=1)    
    text = reader.readtext(cv_img)
    
    for z in range(0,len(text)):
        for i in range(0,4):
            for j in range(0,2):
                text[z][0][i][j] = int(text[z][0][i][j])
                
    final_text = fix_text(make_1line(text), fix_dict_lst)
    # final_text = make_1line(text)
                
    return json.dumps(final_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8503)