# # # from functools import wraps
# # # import tracemalloc
# # # import psutil
# # from time import perf_counter


# # # def measure_performance(func):
# # #     '''Measure CPU and RAM Performance of a Function'''

# # #     @wraps(func)
# # #     def wrapper(*args, **kwargs):
# # #         tracemalloc.start()
# # #         start_time = perf_counter()
# # #         func(*args, **kwargs)
# # #         current, peak = tracemalloc.get_traced_memory()
# # #         finish_time = perf_counter()
# # #         print(f'Function: {func.__name__}')
# # #         print(f'Method: {func.__doc__}')
# # #         print(f'Memory usage:\t\t {current / 10**6:.6f} MB \n'
# # #               f'Peak memory usage:\t {peak / 10**6:.6f} MB ')
# # #         print(f'CPU Usage: {psutil.cpu_percent()} %')
# # #         print(f'RAM Usage: {psutil.virtual_memory().total-psutil.virtual_memory().available}')
# # #         print(f'RAM Usage: {psutil.virtual_memory().percent} %')
# # #         print(f'Time elapsed is seconds: {finish_time - start_time:.9f}')
# # #         print(f'{"-"*40}')
# # #         tracemalloc.stop()
# # #     return wrapper


# # # @measure_performance
# # # def make_list1():
# # #     '''Range'''

# # #     my_list = list(range(100000))


# # # @measure_performance
# # # def make_list2():
# # #     '''List comprehension'''

# # #     my_list = [l for l in range(100000)]


# # # @measure_performance
# # # def make_list3():
# # #     '''Append'''

# # #     my_list = []
# # #     for item in range(100000):
# # #         my_list.append(item)


# # # @measure_performance
# # # def make_list4():
# # #     '''Concatenation'''

# # #     my_list = []
# # #     for item in range(100000):
# # #         my_list = my_list + [item]


# # # print(make_list1())
# # # print(make_list2())
# # # print(make_list3())
# # # print(make_list4())
# # import threading
# # import concurrent.futures


# # import threading
# # import concurrent.futures
# # import time

# # startTime = time.perf_counter()

# # def do_something(second):
# #     print(f"Sleeping {second} second(s)...")
# #     time.sleep(second)
# #     return f"Done Sleeping for {second}"


# # # thread1 = threading.Thread(target=do_something); thread2 = threading.Thread(target=do_something);

# # # thread1.start(); thread2.start();
# # # thread1.join(); thread2.join();

# # with concurrent.futures.ThreadPoolExecutor() as executor:
# #     # f1 = executor.submit(do_something, 1)
# #     # f2 = executor.submit(do_something, 2)
# #     # print(f1.result())
# #     # print(f2.result())
# #     # result = [executor.submit(do_something, i) for i in range(1,3)]

# #     # for  f  in concurrent.futures.as_completed(result):
# #     #     f.result()
# #     secs = [5, 4, 3, 2, 1]
# #     results = executor.map(do_something, secs)

# #     # for result in results:
# #     #     print(result)

# # # threads = []
# # # for _ in range(10):
# # #     t = threading.Thread(target=do_something, args=[1.5])
# # #     t.start();
# # #     threads.append(t)

# # # for thread in threads:
# # #     thread.join();

# # executionTime = (time.perf_counter() - startTime)

# # print(f"Execution Time(seconds): {executionTime} ")


import os
import time
from time import perf_counter
import csv
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


def run_predict(M, T, EM):
    # print(T)
    # print(EM)
    global Val
    Val = 0.0
    print(Val)
    my_list = []
    for item in range(10000):
        my_list.append(item)

    for _ in range(3):
        my_list = []
        for item in range(10000):
            my_list.append(item)
        time.sleep(0.01)

    Val += 2

    print(Val)


def Plot_Metrics(exercise_title: str, model_name: str, cpu: list, memory: list):
    cpu_figure, cpu_ax = plt.subplots()
    cpu_title = f"{exercise_title} - CPU Utilization for Model: {model_name}"
    cpu_index = [i for i in range(len(cpu))]

    memory_figure, memory_ax = plt.subplots()
    memory_title = f"{exercise_title} - Memory Utilization for Model: {model_name}"
    memory_index = [i for i in range(len(memory))]

    cpu_name = f"{exercise_title}_CPU_Model_{model_name}.png"
    memory_name = f"{exercise_title}_Memory_Model_{model_name}.png"

    cpu_ax.plot(cpu_index, cpu, color='cyan')
    cpu_ax.set(title=cpu_title, ylabel='CPU Utilization(%)',
               xlabel='Milliseconds (ms)')
    # cpu_ax.set_xlim(left=max(0, index - 50), right=index + 50)
    cpu_ax.grid(True)

    memory_ax.plot(memory_index, memory, color='orange')
    memory_ax.set(title=memory_title,
                  ylabel='Memory Utilization(%)', xlabel='Milliseconds (ms)')
    # memory_ax.set_xlim(left=max(0, index - 50), right=index + 50)
    memory_ax.grid(True)

    # cpu_figure.canvas.draw()
    # cpu_figure.show()

    # memory_figure.canvas.draw()
    # memory_figure.show()

    # plt.pause(0.05)

    cpu_figure.savefig(
        f"./models/benchmark/{exercise_title}/{model_name}/{cpu_name}", bbox_inches='tight')

    memory_figure.savefig(
        f"./models/benchmark/{exercise_title}/{model_name}/{memory_name}", bbox_inches='tight')
    plt.close('all')


def Resource_Monitor(Exercise: dict, model: str):

    # for i in Exercise:
    #     print(f'{i}: {Exercise[i]}')

    # Log CPU and Memory Usage of `worker_process` every 1 ms
    cpu, memory = [], []
    index = 0
    
    target_process = mp.Process(name="Accuracy Process",target=run_predict, args=(
        model, Exercise_dict['Exercise Title'], Exercise_dict[f'{model} Models']))
    target_process.start() # Child Process
    print(f'Worker Process: {target_process}')
       
    resource_monitor_process = psutil.Process(target_process.pid)
    print(f"Target Parent Process(PPID): {os.getppid()}")
    print(f"Target Process(PID): {target_process.pid}")
    print(f"Resource Monitor Process(PID): {resource_monitor_process.pid}")
    print(f"Process ID(PPID): {resource_monitor_process.ppid()}")

    while target_process.is_alive():
        # print(target_process.is_alive())    
        # while resource_monitor_process.is_running():
        try:
            # cpu.append(psutil.cpu_percent()), memory.append(
            #     psutil.virtual_memory().percent)
            cpu.append((resource_monitor_process.cpu_percent()/ psutil.cpu_count())), memory.append(
            (resource_monitor_process.memory_percent()))

            time.sleep(1e-3)
                
        
        except Exception as exception:
            print(f"Index: {index}\tException: {exception}")
            # continue
        finally:
            index += 1

    target_process.join()
    
    print(f'CPU Usage:\n{cpu}')
    print(f'Memory Usage:\n{memory}')
    print(f"\nIndex: {index}\n")

    Plot_Metrics(Exercise['Exercise Title'], model, cpu, memory)
    # return cpu_percents


if __name__ == '__main__':

    exercise_list = convert_to_dict("Benchmark.csv")

    for Exercise in EXERCISES_FOLDERS:

        try:
            Exercise_dict = exercise_list[Exercise[9:10]]

        except:
            print("Failed to extract values.")

        print(f'\nExercise: {Exercise}')

        for model in MODELS:
            print(f'Model: {model}')

            # with concurrent.futures.ThreadPoolExecutor() as executor:

            #     executor.map(Resource_Monitor, [Exercise_dict, model])
                
            #     print(executor.results())
            Resource_Monitor(Exercise_dict, model)


# import multiprocessing
# import time
# import sys

# import psutil

# def Plot_Metrics(exercise_title: str, model_name: str, cpu: list, memory: list):
#     cpu_figure, cpu_ax = plt.subplots()
#     cpu_title = f"{exercise_title} - CPU Utilization for Model: {model_name}"
#     cpu_index = [i for i in range(len(cpu))]

#     memory_figure, memory_ax = plt.subplots()
#     memory_title = f"{exercise_title} - Memory Utilization for Model: {model_name}"
#     memory_index = [i for i in range(len(memory))]

#     cpu_name = f"{exercise_title}_CPU_Model_{model_name}.png"
#     memory_name = f"{exercise_title}_Memory_Model_{model_name}.png"

#     cpu_ax.plot(cpu_index, cpu, color='cyan')
#     cpu_ax.set(title=cpu_title, ylabel='CPU Utilization(%)',
#                xlabel='Milliseconds (ms)', ylim=[0, 100])
#     # cpu_ax.set_xlim(left=max(0, index - 50), right=index + 50)
#     cpu_ax.grid(True)

#     memory_ax.plot(memory_index, memory, color='orange')
#     memory_ax.set(title=memory_title,
#                   ylabel='Memory Utilization(%)', xlabel='Milliseconds (ms)')
#     # memory_ax.set_xlim(left=max(0, index - 50), right=index + 50)
#     memory_ax.grid(True)

#     # cpu_figure.canvas.draw()
#     # cpu_figure.show()

#     # memory_figure.canvas.draw()
#     # memory_figure.show()

#     # plt.pause(0.05)

#     cpu_figure.savefig(
#         f"./models/benchmark/{cpu_name}", bbox_inches='tight')

#     memory_figure.savefig(
#         f"./models/benchmark/{memory_name}", bbox_inches='tight')
#     plt.close('all')
    
    
# def daemon():
#     cpu, memory = [], []
#     index:int = 0
    
#     p = multiprocessing.current_process()
#     print (f'Starting {p.name} with PID: {os.getpid()}')
#     monitor_process = psutil.Process(os.getpid())
    
#     while monitor_process.is_running():
#         try:
#             index += 1
#             cpu.append(monitor_process.cpu_percent()), memory.append(monitor_process.memory_percent())
#             time.sleep(1e-2)
        
#         except Exception as exception:
#             index += 1
#             print(f"Index: {index}\t Exception: {exception}")
            
            
#     print("CPU:")
#     print(cpu)    
#     print("Memory:")
#     print(memory)    
    
#     Plot_Metrics("E","M",cpu,memory)
    

# def non_daemon():
#     p = multiprocessing.current_process()
#     print (f'Starting {p.name} with PID: {p.pid}')
#     sys.stdout.flush()
#     print (f'Exiting {p.name} with PID: {p.pid}')
#     sys.stdout.flush()

# if __name__ == '__main__':
    
#     n = multiprocessing.Process(name='non-daemon', target=non_daemon)
#     n.daemon = False
    
#     d = multiprocessing.Process(name='daemon', target=daemon)
#     d.daemon = True

#     d.start()
#     print(f"d: {d}, PID: {d.pid}")
#     time.sleep(1)
#     n.start()
#     print(f"n: {n}, PID: {n.pid}")
    

#     d.terminate()
#     n.join()
#     d.join()
# from functools import wraps
# def profiler(func):
#     """CPU and Memory Profiler

#     Args:
#         func (_type_): Python Method to Profile
#     """
#     @wraps(func)
#     def wrapper(*args,**kwargs):
#         print(*args)
#         startTime = time.perf_counter()
#         func(*args,**kwargs)
#         print(f"Function Name: {func.__name__}")
#         cpu, memory = [], []
#         index = 0
#         profiler_process = psutil.Process(os.getpid())
#         print(profiler_process)
#         while profiler_process.is_running():
#             try:
#                 index += 1
#                 cpu.append(profiler_process.cpu_percent()/psutil.cpu_count()), memory.append(profiler_process.memory_percent())
#                 time.sleep(1e-3)
                
#             except Exception as exception:
#                 index += 1
#                 print(f"Index: {index}\nException: {exception}")
#         executionTime = (time.perf_counter()-startTime)
        
#         print(f"CPU:\n{cpu}")
#         print(f"Memory:\n{memory}")
        
#         print(f"Execution Time: {executionTime} seconds")
        
#     return wrapper

# @profiler
# def run_predict(M, T, EM):
#     print(M)
#     print(T)
#     print(EM)
#     global Val
#     Val = 0.0
#     print(Val)
#     my_list = []
#     for item in range(10000):
#         my_list.append(item)

#     for _ in range(3):
#         my_list = []
#         for item in range(10000):
#             my_list.append(item)
#         time.sleep(0.01)

#     Val += 2

#     print(Val)


# if __name__ == '__main__':
#     p = mp.Process(name="Target Function", target=run_predict,args=("ConvLSTM", "Extending the Fingers","ConvLSTM_Extending the Fingers"))
#     print(f"Process: {p} with PID: {p.pid}")
#     p.start()
#     p.join()

