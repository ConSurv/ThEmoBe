#!/usr/bin/env bash

#downloading and extracting face detector model
cd ~/ThEmoBe_basic

wget https://s3-us-west-2.amazonaws.com/static.pyimagesearch.com/face-detection-opencv-deep-learning/deep-learning-face-detection.zip

unzip deep-learning-face-detection.zip



#downloading GSOM code
%cd ~/ThEmoBe_basic

git clone https://github.com/AathmanT/Parallel_GSOM_for_HAAP.git



#downloading YOLO V3 model
cd ~/ThEmoBe_basic

git clone https://github.com/AathmanT/CVND_Exercises_2_2_YOLO.git

wget -O yolov3.weights https://pjreddie.com/media/files/yolov3.weights




pip3 install -r requirements.txt