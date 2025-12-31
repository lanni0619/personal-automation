import os

def make_folder(map):
    for path in map.values():
        if not os.path.exists(path):
            os.makedirs(path)