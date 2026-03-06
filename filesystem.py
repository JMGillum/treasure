import os

def ImmediateSubDirectories(path):
    return [f.name for f in os.scandir(path) if f.is_dir()]

def AllRegularFiles(path):
    return [f.name for f in os.scandir(path) if f.is_file()]
