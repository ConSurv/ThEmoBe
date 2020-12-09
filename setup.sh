#!/usr/bin/env bash

#downloading and extracting face detector model
cd ~/ThEmoBe_basic

wget https://s3-us-west-2.amazonaws.com/static.pyimagesearch.com/face-detection-opencv-deep-learning/deep-learning-face-detection.zip

unzip -f deep-learning-face-detection.zip



#downloading GSOM code
%cd ~/ThEmoBe_basic

git clone https://github.com/AathmanT/Parallel_GSOM_for_HAAP.git



#downloading YOLO V3 model
cd ~/ThEmoBe_basic

git clone https://github.com/AathmanT/CVND_Exercises_2_2_YOLO.git

#wget -O yolov3.weights https://pjreddie.com/media/files/yolov3.weights
cp "/content/drive/My Drive/yolov3.weights" "/content/ThEmoBe/"



pip3 install -r requirements.txt

rm -rf /var/lib/mysql

export DEBIAN_FRONTEND=noninteractive

apt-get update --fix-missing
apt-get install mysql-server
apt-get install libmysqlclient-dev

pip3 install mysqlclient

/etc/init.d/mysql restart

mysql -u root -proot -e "create database annotate";

apt-get install redis-server

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

echo | redis-server &


