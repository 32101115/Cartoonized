#sudo lsof -i :5000 | grep "python" | cut -d " " -f3 | xargs kill -9
#source bin/activate at jitaekim/myproject/venv
#excute main.py
#deaticate
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
import numpy as np

import os
import errno

from os import path
import json
import base64
import webbrowser


import final as f
from flask import Flask, render_template, jsonify,request, redirect,url_for
app = Flask(__name__)

SRC_FOLDER = "input/sample"



OUT_FOLDER = "static"
EXTENSIONS = set(["bmp", "jpeg", "jpg", "png", "tif", "tiff"])
src_contents = os.walk(SRC_FOLDER)
dirpath, _, fnames = src_contents.next()

image_dir = os.path.split(dirpath)[-1]
output_dir = os.path.join(OUT_FOLDER, image_dir)


@app.route('/')
def index():
	return render_template('toonify.html')


@app.route('/toonify/')
def main():
	img = cv2.imread("input.png")
	filtered_image = f.filtering(img)
	edged_image = f.edgeDetection(img)
	filtered_image_with_color = f.quantizeColor(filtered_image,24,5)
	output = f.recombine(filtered_image_with_color,edged_image)

	cv2.imwrite(path.join(OUT_FOLDER, "output.png"), output)
	#cv2.imwrite("output.png", output)

	return jsonify(result="toonify done")

@app.route('/get_img')
def get_img():
	base64_image_str = request.args.get('imgdata')
	base64_image_str= base64_image_str[base64_image_str.find(",")+1:]

	image_64_decode = base64.decodestring(base64_image_str) 
	image_result = open('input.png', 'wb') # create a writable image and write the decoding result
	image_result.write(image_64_decode)

	return jsonify(result="success")

@app.route('/display.html')
def display():
	print('works')
	return render_template('display.html')



if __name__ == "__main__":
	app.run(debug=True)