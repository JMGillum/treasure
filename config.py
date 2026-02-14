import tomllib
import platform
from pathlib import Path
import os


def ExtractConfigItem(config, key, default_value=None):
    try:
        config[key]
        return True
    except KeyError:
        config[key] = default_value
        return False


def DefaultConfigPath(directory_name):
    if platform.system() == "Linux":
        p = Path.home() / ".config" / directory_name
        return p
    return None


def CreateDirectories(dir):
    # Create directories
    dir.mkdir(parents=True, exist_ok=True)
    # os.makedirs(dir,exist_ok=True)


def CreateConfig(contents, filename, directory_name):
    dir = DefaultConfigPath(directory_name)
    if dir is None:
        print("system not detected")
        return False
    # Creates the file path if needed.
    try:
        CreateDirectories(dir)
    except PermissionError:
        print(f"Permission denied: Unable to create '{dir}'.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    path = dir / Path(filename)
    with open(path, "w") as f:
        f.write(contents)
    return True


def FetchConfig(filename, directory_name):
    dir = DefaultConfigPath(directory_name)
    if dir is None:
        print("system not detected")
        return None

    path = dir / Path(filename)
    try:
        with path.open() as f:
            content = f.read()
            x = tomllib.loads(content)
        return x
    except FileNotFoundError:
        return None
