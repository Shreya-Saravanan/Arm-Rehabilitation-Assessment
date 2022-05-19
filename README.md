# Arm Rehabilitation Assessment
 ### <ins>**Goal**</ins>
Our objective is to develop a Web Application that utilizes Deep Learning Models to assess the extent of recovery in hemiplegic patients undergoing Arm-Rehabilitation Exercises.

### <ins>**Workflow**</ins>
The project can be split into four stages:
- Dataset Preparation  
- Best Model Training 
- Web Application Development
- Integrating the Deep Learning Models with the Web Application

### <ins>**Dataset Workflow**</ins>
- The Exercise Process was classified into three stages:
    - <ins>Stage 1:</ins> Patient brings their arm from the initial position to the resting position where they will be performing the exercise.
    - <ins>Stage 2:</ins> The patient has to remain in the position for a duration of time while performing the exercise.
    - <ins>Stage 3:</ins> The patient brings back their arm back to the initial position.
- The eight exercises vary in two aspects:
    - The region of arm where the rehabilitation is focussed on.
    - Camera Position.
- Each Exercise has been classified into four stages of recovery:
    - Recovery Stage: 0 - 25%
        - The patient is unable to perform Stage 1 of the exercise.
        - Implies that the patient is subjected to discomfort while attempting to perform the exercise and requires more practice.
        
    - Recovery Stage: 25 - 50%
        - The patient is unable to perform Stage 2 of the exercise without experiencing discomfort.
        - Implies that the patient is able to perform the exercise but is unable to complete it due to the discomfort experienced.
        
    - Recovery Stage: 50 - 75%
        - The patient is able to perform till Stage 3 of the exercise but takes a lot of time.
        - Implies that the patient is able to make use of their arm muscles albeit with some significant amount of effort.
        
    - Recovery Stage: 75 - 100%
        - The patient is able to perform till Stage 3 of the exercise with relative ease.
        - Implies that the patient is has recovered to a considerable extent and should consult with their medical professional about their recovery progress.


### <ins>**Arm Rehabilitation Exercises:**</ins>
- Arm Placed in the Front       
    ![Arm Placed in the Front](/static/images/I1.png)
- Arm Placed on its Side
    ![Arm Placed on its Side](/static/images/I2.png)
- Extending the Elbow - 1
    ![Extending the Elbow - 1](/static/images/I3.png)
- Extending the Elbow - 2
    ![Extending the Elbow - 2](/static/images/I4.png)
- Turning the Forearm
    ![Turning the Forearm](/static/images/I5.png)
- Extending the Wrist
    ![Extending the Wrist](/static/images/I6.png)
- Extending the Fingers
    ![Extending the Fingers](/static/images/I7.png)
- Extending the Thumb
    ![Extending the Thumb](/static/images/I8.png)


### <ins>**Web Application:**</ins>
- The Web Application was built using Flask which is a very popular Python Framework and HTML, CSS and JavaScript.
- OpenCV and Tensorflow is used for Deep Learning Model integration with the Web Application.
- The application makes use of Moviepy, imageio-ffmpeg, ffmpeg and pymediainfo to process the video recordings of the patient uploading to the server.
- Yagmail, Flask-Mail, ssl and keyring are used to setup the mailing service to provide assessment results for the patient to track their recovery progress and also for medical professionals, updates on their patient's recovery.
