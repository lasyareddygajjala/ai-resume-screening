import os
import shutil

def save_file(upload_file, folder="uploads"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, upload_file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path