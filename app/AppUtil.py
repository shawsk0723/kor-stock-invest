import os
from AppLogger import LOG

def makeDirIfNotExist(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except Exception as e:
        LOG(str(e))