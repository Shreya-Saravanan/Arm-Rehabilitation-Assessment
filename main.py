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
import csv


def convert_to_dict(filename):
    """
    Convert a CSV file to a list of Python dictionaries
    """
    # Open a CSV file - note - must have column headings in top row
    datafile = open(filename, newline='')

    # Create DictReader object
    my_reader = csv.DictReader(datafile)

    # Create a regular Python list containing dicts
    list_of_dicts = list(my_reader)

    # Obtain the Exercise Webpages as an Index Parameter
    webpage_dict = dict()

    for i in list_of_dicts:
        webpage_dict[i['Exercise_Webpage']] = i
    # Close original csv file
    datafile.close()

    # Return the list
    return webpage_dict

def display_result(result):
    
    completeCondition = ("Complete" in result)
    incompleteCondition = ("Incomplete" in result)
    partialCondition_25 = ("25" in result)
    partialCondition_50 = ("50" in result)
    partialCondition_75 = ("75" in result)
    
    Messages = {"It's Alright, Don't Give Up. You can do this!\nYour Recovery Rate is less than 25%.":'result_0', 
                "You've got this. Just a little more effort\nYour Recovery Rate is atleast 25% but less than 50%!":'result_25', 
                "You're Halfway through this. Don't Give Up Now!!!\nYour Recovery Rate is atleast 50%!!":'result_50', 
                "You're Almost there. Hang in There!!!\nYour Recovery Rate is atleast 75%!!!":'result_75', 
                "Yay!!!! You have nearly Recovered successfully!!!!":'result_100'}
    
    assessmentResult = list(Messages.items())
    
    if completeCondition:
        return assessmentResult[-1]
    
    if incompleteCondition:
        return assessmentResult[0]
    
    if partialCondition_25:
        return assessmentResult[1]
    
    if partialCondition_50:
        return assessmentResult[2]
    
    if partialCondition_75:
        return assessmentResult[3]

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__,
            # static_folder='web_pages/',
            template_folder='web_pages/')

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

Model_Path = os.path.abspath(os.path.expanduser(
    os.path.expandvars('models/conv_lstm.h5')))

print(f'\nModel Path: {Model_Path}\n')

Model = load_model(Model_Path)

print("\nModel Loaded Successfully!!!\n")


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
    
    pred_vector = Model.predict(features)
    pred_vec = pred_vector[0].tolist()
    pred_class = pred_vec.index(max(pred_vec))

    return display_result(CLASSES_LIST[pred_class])

@app.route('/display/About.html', methods=['GET'])
def About():
    return render_template('About.html')

@app.route('/display/Exercises.html', methods=['GET'])
def Exercises():
    return render_template('Exercises.html')


exercise_list = convert_to_dict("Exercises.csv")

@app.route('/Exercise/<Exercise_Webpage>', methods=['GET', 'POST'])
def details(Exercise_Webpage):

    try:
        exercise_dict = exercise_list[Exercise_Webpage]

    except:
        return render_template('Error_404.html')

    return render_template("Exercises_Assessment.html", 
                           Exercise = exercise_dict, 
                           webpage_title = exercise_dict['Exercise_Title'])


@app.route('/', methods=['GET'])
def Index():
    return render_template('Index.html')

@app.route('/', methods=['POST'])
def upload_video():
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No video selected for uploading')

        return redirect(request.url)

    else:

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        prediction = pred_video(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        print(prediction)

        flash(prediction[0],prediction[1])

        print(request.form.get('webpage'))

        return details(request.form.get('webpage'))


@app.route('/display/<filename>')
def display_video(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.errorhandler(404)
def Not_Found(e):
    return render_template('Error_404.html')

if __name__ == "__main__":
    
    app.run(debug = True)
