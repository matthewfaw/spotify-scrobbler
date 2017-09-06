import pickle
from datetime import datetime

def _get_filename(obj_name):
    return "%s_%s.pickle"%(obj_name,datetime.now())

def save(obj, obj_name):
    filename = _get_filename(obj_name)
    with open(filename,'wb') as f:
        pickle.dump(obj,f)
    return filename

def load(obj_name):
    with open(obj_name,'rb') as f:
        return pickle.load(f)
