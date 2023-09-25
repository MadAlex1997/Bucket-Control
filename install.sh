!#/usr/bin/bash

sudo apt install git -y
sudo apt install pip -y
pip install sounddevice scipy pyserial opencv-python awscli -y
sudo apt-get install libportaudio2 -y
sudo apt-get update -y
sudo apt-get install ffmpeg libsm6 libxext6  -y
git clone https://github.com/MadAlex1997/Bucket-Control.git -y
sudo chmod 777 Bucket-Control
cd Bucket-Control/
mkdir Waiting
mkdir Sent
mkdir Video
aws configure