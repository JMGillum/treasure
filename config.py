import tomllib
import platform
from pathlib import Path
import os
from .filesystem import CreateDirectories


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

def ParseSpecificationString(string,item_separator=";",key_value_separator=":",allow_dict=True):
    try:
        string = str(string)
    except ValueError:
        return None
    items = string.split(item_separator)
    options = []
    is_dict = False
    for i in range(len(items)):
        item = items[i]
        if item.find(key_value_separator) >= 0:
            if not allow_dict:
                raise ValueError
            if not is_dict:
                if i == 0:
                    is_dict = True
                    options = {}
                else:
                    raise ValueError
            if is_dict:
                split = item.split(key_value_separator)
                if len(split) != 2:
                    raise ValueError
                else:
                    options |= {split[0]:split[1]}

        else:
            if is_dict:
                raise ValueError

    # options is only used for dictionary
    return options if is_dict else items

