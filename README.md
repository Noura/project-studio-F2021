# project-studio-F2021

This project studio explores Emotion AI with large interactive inflatable sculptures. This repo is for collecting code snippets used for this project.

# Setup for Raspberry Pi Zero W

## Install OpenCV 

```console
sudo pip3 install --upgrade opencv-python

sudo apt-get install libatlas-base-dev

sudo apt-get install libhdf5-dev

sudo apt-get install libjasper-dev

sudo apt-get install libqtgui4

sudo pip3 install --upgrade numpy

```

## Other installs

This is what I did to get it working on my raspberry pi zero w.

```console
sudo apt-get install python3-numpy

sudo apt-get install libblas-dev

sudo apt-get install liblapack-dev

sudo apt-get install libatlas-base-dev

sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev

sudo apt-get -y install libxvidcore-dev libx264-dev

sudo apt-get -y install qt4-dev-tools libatlas-base-dev

sudo apt-get install python3-h5py

sudo apt-get install cmake

sudo apt-get install libboost-all-dev

```

Also installed Python libraries

```console
sudo pip3 install cmake

sudo pip3 install dlib

sudo pip3 install face_recognition

sudo pip3 install keras

sudo pip3 install tflite

```

Download the wheel for the custom tensor flow lite build for raspberry pi zero w and install it. 

```console

cd

wget https://github.com/prettyflyforabeeguy/tf_lite_on_pi_zero/blob/master/whl/armv6l/tflite_runtime-2.3.1-cp37-cp37m-linux_armv6l.whl?raw=true

mv 'tflite_runtime-2.3.1-cp37-cp37m-linux_armv6l.whl?raw=true' tflite_runtime-2.3.1-cp37-cp37m-linux_armv6l.whl

sudo pip3 install tflite_runtime-2.3.1-cp37-cp37m-linux_armv6l.whl

```



# Acknowledgements

[Priyanka Dwivedi - Pretrained Emotion Model](https://github.com/priya-dwivedi/face_and_emotion_detection)

[Pretty Fly for a Bee Guy - TFLite on Raspberry Pi Zero](https://github.com/prettyflyforabeeguy/tf_lite_on_pi_zero)
