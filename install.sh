!#/usr/bin/bash

sudo apt install pip -y
sudo pip install sounddevice scipy pyserial opencv-python
curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo bash ./aws/install
sudo apt-get install libportaudio2 -y
sudo apt-get update -y
sudo apt-get install ffmpeg libsm6 libxext6  -y
sudo chmod 777 Bucket-Control
cd Bucket-Control/
sudo mv main.sh /main/main.sh
sudo cp /main/Bucket-Control/rc.local /etc/rc.local
mkdir Waiting
mkdir Sent
mkdir Video
mkdir Data
mkdir Meta
mkdir Not
sudo chmod 777 *
python meta_setup.py
aws configure