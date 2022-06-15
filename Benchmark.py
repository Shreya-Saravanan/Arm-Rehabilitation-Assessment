import os
import random
import csv
import cv2
import numpy as np
from keras.models import load_model
import time
from time import perf_counter
import multiprocessing as mp
import psutil
import matplotlib.pyplot as plt

EXERCISES_FOLDERS: list = ["Exercise 1 - Arm Placed in the Front",
                           "Exercise 2 - Arm Placed on its Side",
                           "Exercise 3 - Extending the Elbow_1",
                           "Exercise 4 - Extending the Elbow_2",
                           "Exercise 5 - Turning the Forearm",
                           "Exercise 6 - Extending the Wrist",
                           "Exercise 7 - Extending the Fingers",
                           "Exercise 8 - Extending the Thumb"]

MODELS: list = ["BiLSTM",
                "ConvLSTM",
                "LRCN",
                "LSTM"]


def convert_to_dict(filename: str):
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
    Exercises_Dict = dict()

    for i in list_of_dicts:
        Exercises_Dict[i['Exercise Number']] = i
    # Close original csv file
    datafile.close()

    # Return the list
    return Exercises_Dict


def Frames_Extraction(video_path: str):
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


def Load_Model(Model_Name: str, Exercise_Title: str, Exercise_Model: str):
    try:
        Model_Path = os.path.abspath(os.path.expanduser(
            os.path.expandvars(f'./models/benchmark/{Exercise_Title}/{Model_Name}/{Exercise_Model}')))
        print(f'\nModel Path: {Model_Path}\n')

        Model = load_model(Model_Path)
        print(f"{Model_Name} Model for {Exercise_Title} Loaded Successfully!!!\n")

        return Model

    except:
        pass


def Predict_Video(Model_Name: str, Exercise_Title: str, Exercise_Model: str, video_file: str):

    Model = Load_Model(Model_Name, Exercise_Title, Exercise_Model)

    SEQUENCE_LENGTH = 40

    CLASSES_LIST = ["C_25", "C_50", "C_75", "C_100"]

    features = []

    frames = Frames_Extraction(video_file)

    if len(frames) == SEQUENCE_LENGTH:
        features.append(frames)

    features = np.asarray(features)

    pred_vector = Model.predict(features)
    pred_vec = pred_vector[0].tolist()
    pred_class = pred_vec.index(max(pred_vec))

    print(CLASSES_LIST[pred_class])

    return (CLASSES_LIST[pred_class])


def Accuracy(Model_Name: str, Exercise_Title: str, Model: str):
    global Model_Accuracy

    path = f'./static/uploads/benchmark/{Exercise_Title}/'
    Files = len(os.listdir(path))  # Number of Files present in the Folder
    print(f"N: {Files}")
    startTime = perf_counter()

    filenames = random.sample(os.listdir(path), k=Files)

    print(f"Number of Files: {Files} at Path: {path}")
    print(f"Filenames:\n", *filenames, sep='\n')

    count, tp_count = 0, 0

    for filename in filenames:
        prediction = Predict_Video(
            Model_Name, Exercise_Title, Exercise_Model=Model, filename=filename)

        if prediction in filename:
            count += 1
            tp_count += 1
        else:
            count += 1
    print(f"N': {count}")
    Model_Accuracy = ((tp_count / count) * 100)
    print(f"Accuracy of {Model} Model: {Model_Accuracy} %")
    
    executionTime = (perf_counter() - startTime)
    print(f"Time Elapsed: {executionTime:.9f} seconds\n\n")


def Plot_Metrics(exercise_title: str, model_name: str, cpu: list, memory: list):
    
    cpu_figure, cpu_ax = plt.subplots()
    cpu_title = f"{exercise_title} - CPU Utilization for Model: {model_name}"
    cpu_index = [i for i in range(len(cpu))]

    cpu_name = f"{exercise_title}_CPU_Model_{model_name}.png"
    memory_name = f"{exercise_title}_Memory_Model_{model_name}.png"

    cpu_ax.plot(cpu_index, cpu, color='cyan')
    cpu_ax.set(title=cpu_title, ylabel='CPU Utilization(%)',
               xlabel='Milliseconds (ms)')
    cpu_ax.grid(True)

    cpu_figure.savefig(
        f"./models/benchmark/{exercise_title}/{model_name}/{cpu_name}", bbox_inches='tight')


    memory_figure, memory_ax = plt.subplots()
    memory_title = f"{exercise_title} - Memory Utilization for Model: {model_name}"
    memory_index = [i for i in range(len(memory))]

    memory_ax.plot(memory_index, memory, color='orange')
    memory_ax.set(title=memory_title,
                  ylabel='Memory Utilization(%)', xlabel='Milliseconds (ms)')
    memory_ax.grid(True)

    memory_figure.savefig(
        f"./models/benchmark/{exercise_title}/{model_name}/{memory_name}", bbox_inches='tight')
    plt.close('all')


def Resource_Monitor(Exercise: dict, model: str):

    cpu, memory = [], []
    index = 0
    
    target_process = mp.Process(name="Accuracy Process",target=Accuracy, args=(
        model, Exercise_dict['Exercise Title'], Exercise_dict[f'{model} Models']))
    target_process.start() # Child Process
    print(f'Target Process: {target_process}')
       
    resource_monitor_process = psutil.Process(target_process.pid)
    print(f"Target Parent Process(PPID): {os.getppid()}")
    print(f"Target Process(PID): {target_process.pid}")
    print(f"Resource Monitor Process(PID): {resource_monitor_process.pid}")
    print(f"Process ID(PPID): {resource_monitor_process.ppid()}")

    while target_process.is_alive():
        print(target_process.is_alive())    
        try:

            cpu.append((resource_monitor_process.cpu_percent()/ psutil.cpu_count())), memory.append(
            (resource_monitor_process.memory_percent()))

            # Log CPU and Memory Usage of `target_process` every 1 ms       
            time.sleep(1e-3)
                
        
        except Exception as exception:
            print(f"Index: {index}\tException: {exception}")
            
        finally:
            index += 1

    target_process.join()
    
    print(f'CPU Usage:\n{cpu}')
    print(f'Memory Usage:\n{memory}')
    print(f"\nIndex: {index}\n")
    
    Plot_Metrics(Exercise['Exercise Title'], model, cpu, memory)


if __name__ == '__main__':

    exercise_list = convert_to_dict("Benchmark.csv")

    for Exercise in EXERCISES_FOLDERS:

        try:
            Exercise_dict = exercise_list[Exercise[9:10]]

        except:
            print("Failed to extract values.")

        print(f'\nExercise: {Exercise}')

        for model in MODELS:
            
            # if Exercise_dict['Exercise Number'] in [1,4,7]:      # Change the List Value to run the Benchmark for the desired Exercise  
            #     Resource_Monitor(Exercise_dict, model)
                  
            Resource_Monitor(Exercise_dict, model)

