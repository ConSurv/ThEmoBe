import cv2
import matplotlib.pyplot as plt

from utils import *
from darknet import Darknet

import keras
import cv2
import os
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join, isdir
from PIL import Image
import numpy as np
import shelve
import matplotlib.pyplot as plt


# Set the location and name of the cfg file
cfg_file = '/content/CVND_Exercises/2_2_YOLO/cfg/yolov3.cfg'

# Set the location and name of the pre-trained weights file
weight_file = '/content/drive/My Drive/yolov3.weights'

# Set the location and name of the COCO object classes file
namesfile = '/content/CVND_Exercises/2_2_YOLO/data/coco.names'

# Load the network architecture
m = Darknet(cfg_file)

# Load the pre-trained weights
m.load_weights(weight_file)

# Load the COCO object classes
class_names = load_class_names(namesfile)

def crop_human(img):
  # Set the default figure size
  plt.rcParams['figure.figsize'] = [24.0, 14.0]

  black = img.copy()*0

  width = img.shape[1]
  height = img.shape[0]

  # Convert the image to RGB
  original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  # We resize the image to the input width and height of the first layer of the network.
  resized_image = cv2.resize(original_image, (m.width, m.height))

  # Set the IOU threshold. Default value is 0.4
  iou_thresh = 0.4

  # Set the NMS threshold. Default value is 0.6
  nms_thresh = 0.6

  # Detect objects in the image
  boxes = detect_objects(m, resized_image, iou_thresh, nms_thresh)
  # Print the objects found and the confidence level
  # print_objects(boxes, class_names)
  X1,X2,Y1,Y2 = -1,-1,-1,-1
  A = 0
  if len(boxes) > 0:
    for box in boxes:
      # cropping only human
      if (int(box[6]))==0:
        x1 = int(np.around((box[0]-box[2]/2.0)*width))
        y1 = int(np.around((box[1]-box[3]/2.0)*height))
        x2 = int(np.around((box[0]+box[2]/2.0)*width))
        y2 = int(np.around((box[1]+box[3]/2.0)*height))
        a = (x2-x1)*(y2-y1)
        # Cropping the biggest frame
        if (a>A):
          A = a
          X1,X2,Y1,Y2 = x1, x2, y1, y2
  #Plot the image with bounding boxes and corresponding object class labels
  # plot_boxes(original_image, boxes, class_names, plot_labels = True)

  black[y1:y2, x1:x2] = img[y1:y2, x1:x2]

  return black, [X1,X2,Y1,Y2]