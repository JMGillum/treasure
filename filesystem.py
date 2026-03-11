import os
import hashlib

def ImmediateSubDirectories(path):
    return [f.name for f in os.scandir(path) if f.is_dir()]

def AllRegularFiles(path):
    return [f.name for f in os.scandir(path) if f.is_file()]

def GenerateHash(path,algorithm,block_size=65536):
    if algorithm.strip().lower() == "sha1":
        hasher = hashlib.sha1()
        with open(path, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
                return hasher.hexdigest()

    return None

def CreateDirectories(dir):
    dir.mkdir(parents=True, exist_ok=True)


