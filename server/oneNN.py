import cv2
import os
import glob
import numpy as np
from PIL import Image
from IPython.display import clear_output, display
from imutils.video import VideoStream, FileVideoStream
from tqdm.notebook import tqdm
import time

class OneNNClassifier:
    
    def __init__(self, ids, descs):
      self.ids = ids
      self.descs = descs    

    def predict(self, queryF,username):
        if (self.descs == []):
            return None
        max_score = 0.0
        max_id = ''
        for i in range(0,len(self.descs)):
            if (self.ids[i] == username):
                return None
            score = np.dot(self.descs[i],queryF)
            if (score > max_score):
                max_score = score
                max_id = self.ids[i] 
        if(max_score < 0.70):
            return None
        else:
            return max_id
        
        