import cv2
import os
import glob

import numpy as np

from PIL import Image
from IPython.display import clear_output, display
from imutils.video import VideoStream, FileVideoStream
from tqdm.notebook import tqdm
import time



#Detector parameters
DET_PROTO = './facerecognition/caffe/face_detector/deploy.prototxt'

DET_MODEL = './facerecognition/caffe/face_detector/res10_300x300_ssd_iter_140000_fp16.caffemodel'
DET_LAYER = 'detection_out'
DET_SIZE = (300, 300)
DET_MEAN = (123, 177,104)
DET_THRESHOLD = 0.7

#VGG2 parameters
FEAT_PROTO = './facerecognition/caffe/face_features/resnet50_ft.prototxt'
FEAT_MODEL = './facerecognition/caffe/face_features/resnet50_ft.caffemodel'
FEAT_LAYER = "pool5/7x7_s1"
FEAT_SIZE = (224, 224)
FEAT_MEAN = (91.4953, 103.8827, 131.0912)
PRED_THRESHOLD = 0.7

SRC_FOLDER = './client/registration'

FRAMES_TO_SKIP = 800

GREEN = (0, 255, 0)
RED = (0, 0, 255)

def highlight(img, rect, color, text=None):
    cv2.rectangle(img, rect[0], rect[1], color, 3, 3, 0)
    point = (rect[0][0] - 20, rect[1][1] + 50)
    if text != None:
        cv2.putText(img, text, point, 4, 1.2, color)


def getImageROI(img, face):
    return img[ face[1][1]:face[0][1], face[1][0]:face[0][0]]


def display_img(img, is_bgr=True):
  if is_bgr:  # convert color from CV2 BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
  display(Image.fromarray(img))
  clear_output(wait=True)

class DNNExtractor:    
    
    def __init__(self, net_proto_path, trained_model_path, size, mean_values=None):
        self.size = size
        self.mean_values = mean_values

        self.net = cv2.dnn.readNetFromCaffe(net_proto_path, trained_model_path)
        # to enable GPU (this won't work on Colab without recompiling opencv)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        
    
    def extract(self, img, layer, normalize=False):
        blob = cv2.dnn.blobFromImage(img, 1.0, self.size, self.mean_values, swapRB=False, crop=False)
        self.net.setInput(blob)
        prob = self.net.forward(layer).flatten()

        if normalize:
            prob /= np.linalg.norm(prob)

        return prob
    
# it creates an instance of the class DNNExtractor
det = DNNExtractor(DET_PROTO, DET_MODEL, DET_SIZE, DET_MEAN)
fe = DNNExtractor(FEAT_PROTO, FEAT_MODEL, FEAT_SIZE, FEAT_MEAN)



def extract_average_features(directory_path):
    average_descs = []
    img_paths = glob.glob(directory_path + "/*.jpg")
    descs = [fe.extract(cv2.imread(path), FEAT_LAYER, normalize=True) for path in tqdm(img_paths)]
    desc_dim = len(descs[0])
    sum_vector = np.zeros(desc_dim)
    count_vector = np.zeros(desc_dim)
    average_vector = np.zeros(desc_dim)
    for desc in descs:
        for i in range(0,desc_dim):
            sum_vector[i] += desc[i]
            count_vector[i] += 1
    for i in range(0,desc_dim):
        average_vector[i] = sum_vector[i] / count_vector[i]
    average_descs.append(average_vector/(np.linalg.norm(average_vector)))
    return np.array(average_descs)

def detect(img):
  bbs = det.extract(img, DET_LAYER)
  bbs = bbs.reshape(-1, 7)  # one detection per row
  h,w, _ = img.shape
    
  faces = []

  for batch_id, class_id, confidence, left, top, right, bottom in bbs:
    #check if the confidence value <  DET_THRESHOLD
    #determine points p0 and p1, i.e. the top left and bottom right vertex of the BB, with respect to the original coordinates from the normalized dimensions: left, top, right, bottom 
    if confidence > DET_THRESHOLD:
      denormalized_left = (left * w).astype(int)
      denormalized_top = (top * h).astype(int)
      denormalized_right = (right * w).astype(int)
      denormalized_bottom = (bottom * h).astype(int)

      top_left = ( denormalized_left , denormalized_top )
      bottom_right = ( denormalized_right , denormalized_bottom )

      face = (bottom_right , top_left )

      faces.append(face)


  return faces

def get_average_features(function_type):

    vid = cv2.VideoCapture(0)
    if not vid.isOpened():
        print("Error opening video")
    count=0
    all_features = []
    frame = ""
    directory = ""
    detected_faces = 0
    if(function_type=='registration'):
        directory = './registration'
    else:
        directory = './login'
    while(True):
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        detected_faces = detect(frame)
        if (detected_faces == []):
            vid.release()
            cv2.destroyAllWindows()
            return frame,[],[]
        for detected_face in detected_faces:
            imageROI = getImageROI(frame , detected_face)
            cv2.imwrite(directory+'/img'+str(count)+'.jpg', imageROI, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        count +=1
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        #if cv2.waitKey(1) & 0xFF == ord('q') or count==30:
        if cv2.waitKey(1) & 0xFF == ord('q') or count==10: #solo per test
            break
        time.sleep(1)
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
    average_desc = extract_average_features(directory)
    return frame,detected_faces,average_desc
