import glob
import os

def delete_files_with_extension(directory:str, extension:str):
    PATH = f'{directory}/**/*.{extension}'

    files = glob.glob(PATH, recursive=True)
    print(*files, sep='\n')
    
    for file in files:
        try:
            os.remove(file)
            print(f"File {file} Deleted Successfully!!!")
        
        except OSError:
            os.remove(file)
            
delete_files_with_extension('./static/uploads/benchmark','png')
