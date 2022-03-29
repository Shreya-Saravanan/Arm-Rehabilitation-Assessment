import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from tensorflow import keras
from keras.models import load_model
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.editor as mp

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__, template_folder = 'web_pages/')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

MODEL_PATH = os.path.abspath(os.path.expanduser(
    os.path.expandvars('models/conv_lstm.h5')))
print(MODEL_PATH)

lstm_model = load_model(MODEL_PATH)
print("Model Loaded Successfully!!!")


def frames_extraction(video_path):
    SEQUENCE_LENGTH = 40
    IMAGE_HEIGHT, IMAGE_WIDTH = 64, 64
    frames_list = []
    video_reader = cv2.VideoCapture(video_path)
    video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
    skip_frames_window = max(int(video_frames_count/SEQUENCE_LENGTH), 1)

    for frame_counter in range(SEQUENCE_LENGTH):
        video_reader.set(cv2.CAP_PROP_POS_FRAMES,
                         frame_counter * skip_frames_window)
        success, frame = video_reader.read()

        if not success:
            break

        resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
        normalized_frame = resized_frame / 255
        frames_list.append(normalized_frame)

    video_reader.release()
    return frames_list


def pred_video(video_file):
    SEQUENCE_LENGTH = 40
    CLASSES_LIST = ["Exercise 1 - Arm Placed in the Front - Complete",
                    "Exercise 1 - Arm Placed in the Front - Incomplete",
                    "Exercise 2 - Arm Placed on its Side - Complete",
                    "Exercise 2 - Arm Placed on its Side - Incomplete",
                    "Exercise 4 - Extending the Elbow_1 - Complete",
                    "Exercise 4 - Extending the Elbow_1 - Incomplete",
                    "Exercise 5 - Extending the Elbow_2 - Complete",
                    "Exercise 5 - Extending the Elbow_2 - Incomplete",
                    "Exercise 6 - Turning the Forearm - Complete",
                    "Exercise 6 - Turning the Forearm - Incomplete",
                    "Exercise 7 - Extending the Wrist - Complete",
                    "Exercise 7 - Extending the Wrist - Incomplete",
                    "Exercise 8 - Extending the Fingers - Complete",
                    "Exercise 8 - Extending the Fingers - Incomplete",
                    "Exercise 9 - Extending the Thumb - Complete",
                    "Exercise 9 - Extending the Thumb - Incomplete"]

    features = []
    frames = frames_extraction(video_file)

    if len(frames) == SEQUENCE_LENGTH:
        features.append(frames)

    features = np.asarray(features)
    pred_vector = lstm_model.predict(features)
    pred_vec = pred_vector[0].tolist()
    pred_class = pred_vec.index(max(pred_vec))

    return CLASSES_LIST[pred_class]


# Home Page
@app.route('/')
def mainpage():
    return render_template('Home.html')
# Home Page

@app.route('/Home.html')
def homepage():
    return render_template('Home.html')

@app.route("/")
def favicon():
    return "", 200

# Exercises Page
@app.route('/Exercises.html')
def exercises_page():
    return render_template('Exercises.html')

# Exercise Page
@app.route('/Arm_Placed_in_the_Front.html')
def exercise_page_1():
    return render_template('Arm_Placed_in_the_Front.html') 
   
# Exercise Page
@app.route('/Arm_Placed_on_its_Side.html')
def exercise_page_2():
    return render_template('Arm_Placed_on_its_Side.html') 
   
# Exercise Page
@app.route('/Extending_the_Elbow_1.html')
def exercise_page_3():
    return render_template('Extending_the_Elbow_1.html') 
   
# Exercise Page
@app.route('/Extending_the_Elbow_2.html')
def exercise_page_4():
    return render_template('Extending_the_Elbow_2.html') 
   
# Exercise Page
@app.route('/Extending_the_Fingers.html')
def exercise_page_5():
    return render_template('Extending_the_Fingers.html') 
   
# Exercise Page
@app.route('/Extending_the_Thumb.html')
def exercise_page_6():
    return render_template('Extending_the_Thumb.html') 
   
# Exercise Page
@app.route('/Extending_the_Wrist.html')
def exercise_page_7():
    return render_template('Extending_the_Wrist.html') 
   
# Exercise Page
@app.route('/Turning_the_Forearm.html')
def exercise_page_8():
    return render_template('Turning_the_Forearm.html') 

# About Page
@app.route('/About.html')
def about_page():
    return render_template('About.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('Error_404.html'), 404
# @app.route('/')
# def upload_form():
#     return render_template('upload.html')


# @app.route('/', methods = ['POST'])
# def upload_video():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)

#     file = request.files['file']

#     if file.filename == '':
#         flash('No video selected for uploading')

#         return redirect(request.url)

#     else:
        
#         fileName = os.path.join(app.config['UPLOAD_FOLDER'], _fn)
#         file.save(fileName)
#         _fn = secure_filename(file.filename)
        
#         targetName = os.path.join(app.config['UPLOAD_FOLDER'], 'out_'+_fn)
#         duration = mp.VideoFileClip(fileName).duration

#         ffmpeg_extract_subclip(
#             fileName, 0, (duration - 10), targetname = targetName)

#         pred = pred_video(os.path.join(
#             app.config['UPLOAD_FOLDER'], targetName))
#         flash(pred)

#         return render_template('./web_pages/upload.html', filename = targetName)


# @app.route('/display/<filename>')
# def display_video(filename):
#     return redirect(url_for('static', filename ='uploads/' + filename), code = 301)


if __name__ == "__main__":
    app.run()
