import os

def get_extension(filepath):
    return os.path.splitext(filepath)[1]