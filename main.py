import os, shutil
import urllib.request
from flask import Flask, flash, redirect, request, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from tensorflow import keras
from keras.models import load_model
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import csv
from flaskext.markdown import Markdown
from datetime import datetime
from pymediainfo import MediaInfo
import MailingService


def convert_to_dict(filename:str):
    """Convert a CSV file to a list of Python Dictionaries.

    Args:
        - filename (str): CSV Filename to be read.

    Returns:
        - Exercise (dict): Returns Key-Value Pair of the Exercise details to be loaded by the Web Server.
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


def Delete_File(upload_path:str, filename:str):
    """To Delete the Recording uploaded by User after they receive their assessment result.

    Args:
        - upload_path (str): Folder Path of the Recording.
        - filename (str): File Name of the uploaded Recording.
    """
    try:
        if os.path.exists(upload_path):
            os.remove(upload_path)
            print(f'\nFile {filename} at location {upload_path} deleted successfully\n')
        
        else:
            print(f"The File {filename} does not exist\n")

    except OSError as error:
        print(f"Error: {error}")
        print('\nFile did not get deleted')


def Folder_Clear(Upload_Folder:str): # Delete all files, subdirectories, and symbolic links from a Directory
    """To clear the Web Server 'static/uploads/' Folder in case of any Error 500 instances.

    Args:
     -   Upload_Folder (str): Folder Path to clear the Folder Contents.
    """
    print(f"Scheduler to Clear Folder contents at Path: '{Upload_Folder}'!")
    
    for files in os.listdir(Upload_Folder):
        path = os.path.join(Upload_Folder, files)
        
        try:
            print(f"File {files} Path: {path} Deleted Successfully!!!")
            shutil.rmtree(path)
        
        except OSError:
            os.remove(path)
    print()


def Video_Duration(filename:str):
    """To obtain the duration of the Recording in string format.

    Args:
        - filename (str): File Name of the uploaded Recording.

    Returns:
        - duration (str): Returns Duration of the Video Recording in (hh:mm:ss:ms) Format.
    """
    metadata = MediaInfo.parse('./static/uploads/' + filename)
    
    duration = ''

    for track in metadata.tracks:
        if track.track_type == "Video":
            # print("Bit rate: {t.bit_rate}, Frame rate: {t.frame_rate}, "
            #     "Format: {t.format}".format(t=track)
            # )
            # print("Duration (other values:")
            # print(track.other_duration[4])
            duration = track.other_duration[4]
    # print(f'Duration of the Video: {duration}')
    
    return duration


def SendEmail(recipient_name:str, mailing_list:list, Exercise:str, duration:str, prediction:str):
    """To send Email to User their assessment results.
    Args:
        - recipient_name (str): User Name
        - mailing_list (list): List containing Email IDs to send the Email to.
        - Exercise (str): Name of the Exercise the User undertook the assessment.
        - duration (str): Duration for which the User had undertaken the assessment.
        - prediction (str): Assessment Result 
    """
    if recipient_name == '':
        recipient_name = 'User'

    print('Mailing List: ', *mailing_list, sep = ',')
    subject = f"Your Assessment Results for the Exercise: {Exercise}"

    message = f"""Hello There {recipient_name}!!!
    Your Assessment Result for the Exercise {Exercise} is: {prediction}
    
    Date and Time of the Exercise performed: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    
    Duration of the Exercise performed (hh:mm:ss:ms): {duration}
    
    Hope you have a Nice Day!!!
    """
    print(message)

    MailingService.MailSettings(email_option = email_option, 
                                mailing_list = mailing_list, 
                                subject = subject, 
                                body = message)
    

def Load_Model(Exercise_Models:str):
    """Loads Keras Model for the specified Exercise.

    Args:
        - Exercise_Models (str): File Path of the Exercise Model.

    Returns:
        - Model (Keras Model): Returns a Keras Model used to predict the uploaded Recording.
    """
    Model_Path = os.path.abspath(os.path.expanduser(
    os.path.expandvars('models/' + Exercise_Models)))

    print(f'\nModel Path: {Model_Path}\n')
    Model = load_model(Model_Path)
    print(f"Model for Exercise {int(Exercise_Models[9:10])} Loaded Successfully!!!\n")
    
    return Model


def Frames_Extraction(video_path:str):
    """To extract the frames from Recording to pass into the Keras Model.

    Args:
        - video_path (str): Video Recording File Path.

    Returns:
        - frames (list): Returns a list of all the frames in the Recording.
    """
    SEQUENCE_LENGTH = 40
    IMAGE_HEIGHT, IMAGE_WIDTH = 70, 70

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


def Display_Result(result:str):
    """Message to be displayed to the Web Application.

    Args:
        - result (str): Result from the predicted recording.

    Returns:
        - (Result, Category) (list[str, str]) : Returns the prediction result and category for flashing the message in Web Application.
    """
    completeCondition = ("100" in result)
    partialCondition_25 = ("25" in result)
    partialCondition_50 = ("50" in result)
    partialCondition_75 = ("75" in result)
    
    Messages = ["It's Alright, Don't Give Up. You can do this!\nYour Recovery Rate is less than 25%.", 
                "You've got this. Just a little more effort\nYour Recovery Rate is at least 25 - 50%!",
                "You're Halfway through this. Don't Give Up Now!!!\nYour Recovery Rate is at least 50 - 75%!!",
                "Yay!!!! You have nearly Recovered Successfully!!!!\nYour Recovery Rate is more than 75%!!! "]
    
    predictionResult = {Messages[0]:'result_25',
                        Messages[1]:'result_50',
                        Messages[2]:'result_75',
                        Messages[-1]:'result_100'}
                        
    
    assessmentResult = list(predictionResult.items())
    
    if completeCondition:
        return assessmentResult[-1]
    
    if partialCondition_25:
        return assessmentResult[0]
    
    if partialCondition_50:
        return assessmentResult[1]
    
    if partialCondition_75:
        return assessmentResult[2]


def Predict_Video(Exercise_Models:str, video_file:str):
    """Predict the extent of User recovery using the Recording passed to Keras Model.

    Args:
        - Exercise_Models (str): Exercise Model Used.
        - video_file (str): Video Recording File Path.

    Returns:
        - _type_: Assessment Results.
    """
    Model = Load_Model(Exercise_Models)
    
    SEQUENCE_LENGTH = 40
    
    CLASSES_LIST = ["Complete_25", "Complete_50", "Complete_75", "Complete_100"]

    features = []

    frames = Frames_Extraction(video_file)

    if len(frames) == SEQUENCE_LENGTH:
        features.append(frames)

    features = np.asarray(features)

    pred_vector = Model.predict(features)
    pred_vec = pred_vector[0].tolist()
    pred_class = pred_vec.index(max(pred_vec))

    print(CLASSES_LIST[pred_class]) 
    return Display_Result(CLASSES_LIST[pred_class])


def Flash_Prediction(Exercise_Model:str, filename:str):
    """Flash User Assessment Results in Flask Web Application.

    Args:
        - Exercise_Model (str): Exercise Model used.
        - filename (str): Video Recording File Path

    Returns:
        - upload_path (str): Video Recording File Path to be deleted after flashing the message in Web Application.
        - prediction (list[str, str]): Returns the prediction result and category for flashing the message in Web Application.
    """
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f'\nUpload Path: {upload_path}\n')
    prediction = Predict_Video(Exercise_Model, upload_path)
    
    return upload_path, prediction
    

app = Flask(__name__,
            # static_folder='web_pages/',
            template_folder='web_pages/')

app.secret_key = os.urandom(24).hex()
app.config['UPLOAD_FOLDER'] = './static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 # 100 MB Size Limit for the Video File to be Uploaded

# Mail Settings
email_option:int = 1
admin_email = ['flask_web_app_fyp@outlook.com',
               'fyp.send.email.web.app.flask@gmail.com'
               ]
recipient_name = ''
recipient_email = ''

Markdown(app)


exercise_list = convert_to_dict("Exercises.csv")

@app.route('/display/About.html', methods=['GET'])
def About():
    return render_template('About.html')

@app.route('/Exercise/<Exercise_Webpage>', methods=['GET'])
def Exercise(Exercise_Webpage):
    """Render the Exercise Webpage dynamically.

    Args:
        - Exercise_Webpage (_type_): Used to load the corresponding key-value pair details associated with the Exercise.

    Returns:
        _type_: Returns a template to display the Exercise Webpage.
    """
    print(f'Webpage GET: {Exercise_Webpage}')
    
    try:
        exercise_dict:dict = exercise_list[Exercise_Webpage]

    except:
        return render_template('Error_404.html')

    img_link:str = "images/" + exercise_dict['Image']
    
    with  open("static/instructions/" + exercise_dict['Instructions'], "r", encoding = 'utf-8') as file:
        instruction =  file.read()
        
    with  open("static/instructions/Upload Section.md", "r", encoding = 'utf-8') as file:
        upload_instruction =  file.read()
        
    return render_template("Exercises_Assessment.html", 
                        Exercise = exercise_dict, 
                        webpage_title = exercise_dict['Exercise_Title'],
                        Instructions = instruction, 
                        Upload_Instruction = upload_instruction,
                        Image = img_link)

@app.route('/Exercise/<Exercise_Webpage>',methods=['POST'])
def Exercise_Assessment(Exercise_Webpage):
    """Obtain User assessment recording to provide feedback.

    Returns:
        _type_: Renders a template to display the Webpage with the assessment result flashed as a message.
    """
    print(f"Webpage POST: {request.form['Webpage']}")

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    print(f"File: {file}")
    
    print(f"Form: {request.form}")
    Model = request.form['Model']
    print(f"Model: {Model}")
      
        
    if file.filename == '':
        flash('No Video Selected for Uploading')

        return redirect(request.url)

    else:
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        file_recording = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        
        try:
            if "_live_recording" in file_recording: # Live Recording    
                index = file_recording.rfind('_')
                
                if ".mp4" in file_recording:
                    duration = (file_recording[(index + 1):-4])
                    live_filename = filename[:(filename.find('_live_recording'))] + '.mp4'
                    
                duration = int(duration)
                
                print(f'\nDuration: {duration} seconds\n')

                targetName = os.path.join(app.config['UPLOAD_FOLDER'], live_filename)
                
                ffmpeg_extract_subclip(file_recording, 0, (duration - 10), targetname = targetName)
                live_upload_path = str(file_recording)
                
                print(f'File Name: {filename}')
                print(f'Live Video File Name: {live_filename}')
                print(f'Target Name: {targetName}')
                print(f'\nLive Video File Path: {live_upload_path}')
                
                upload_path, prediction = Flash_Prediction(Exercise_Model = Model, filename = live_filename)
                
                print(prediction)

                flash(prediction[0], prediction[1])       
                
                video_duration = Video_Duration(live_filename)         
                
                print('Upload Recording')
                Delete_File(live_upload_path, filename)
                Delete_File(upload_path, live_filename)
                
                print(f"Upload Recording Details: {request.form['Webpage']}")
                
                
                try:
                    SendEmail('', *admin_email, request.form['Exercise_Name'], video_duration, prediction[0])
                
                except:
                    # Function to clear folder contents when Error 500 occurs
                    print('Error 500')
                    Folder_Clear('./static/uploads/')
    
            
            else:    # Upload Recording 
                if "_upload_recording" in file_recording: # Live Recording    
                    index = file_recording.rfind('_')
                    
                    if ".mp4" in file_recording:
                        duration = (file_recording[(index + 1):-4])
                        live_filename = filename[:(filename.find('_upload_recording'))] + '.mp4'
                        
                    duration = int(duration)
                    
                    print(f'\nDuration: {duration} seconds\n')

                    targetName = os.path.join(app.config['UPLOAD_FOLDER'], live_filename)
                    
                    ffmpeg_extract_subclip(file_recording, 0, (duration - 10), targetname = targetName)
                    live_upload_path = str(file_recording)
                    
                    print(f'File Name: {filename}')
                    print(f'Live Video File Name: {live_filename}')
                    print(f'Target Name: {targetName}')
                    print(f'\nLive Video File Path: {live_upload_path}')
                    
                    upload_path, prediction = Flash_Prediction(Exercise_Model = Model, filename = live_filename)
                    
                    print(prediction)

                    flash(prediction[0], prediction[1])     
                    
                    video_duration = Video_Duration(live_filename)           
                    
                    print('Upload Recording')
                    Delete_File(live_upload_path, filename)
                    Delete_File(upload_path, live_filename)
                
                else:
                    upload_path, prediction = Flash_Prediction(Exercise_Model = Model, filename = filename)
                                    
                    print(prediction)

                    flash(prediction[0], prediction[1])
                    
                    video_duration = Video_Duration(filename)
                    
                    Delete_File(upload_path, filename)
                    
                
                recipient_name, mailing_list = Email()
                
                print(f"Upload Details: {request.form['Webpage']}")
                
                print(f'Duration: {duration}')

                try:
                    SendEmail(recipient_name, mailing_list, request.form['Exercise_Name'], video_duration, prediction[0])
                
                except:
                    # Function to clear folder contents when Error 500 occurs
                    print('Error 500')
                    Folder_Clear('./static/uploads/')
                    
            return Exercise(request.form['Webpage'])

        except:
            prediction = ["Uh-oh, there seems to be a problem", 'result_0']
            return render_template('Error_500.html')

def Email():
    """To Create a Mailing List to send Emails.

    Returns:
        - recipient_name (str): Returns the Name of the Recipient if specified by the User.
        - mailing_list (list[str]): Returns the list of Email IDs to send the Email regarding the Exercises Assessment.
    """
    if request.form['Recipient_Name'] == '':            
        recipient_name = ''
        mailing_list = [*admin_email]
    
    else:
        recipient_name = request.form['Recipient_Name']   
        mailing_list = [request.form['Recipient_Email'], *admin_email]
        
    return recipient_name, mailing_list
        

@app.route('/', methods=['GET'])
def Index():
    return render_template('Index.html')

@app.errorhandler(403)
def Forbidden(e):
    return render_template('Error_403.html'),403

@app.errorhandler(404)
def Not_Found(e):
    return render_template('Error_404.html'),404

@app.errorhandler(408)
def Server_Timeout(e):
    return render_template('Error_408.html'),408

@app.errorhandler(500)
def Internal_Server_Error(e):
    return render_template('Error_500.html'),500

if __name__ == "__main__":
    
    app.run(debug = False)
