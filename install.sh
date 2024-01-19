#!/bin/bash

# Leave current git directory
cd ..

# Create folder for audio recordings
mkdir records
# Create folder and file for logs: senergy, model, temperature
mkdir logs
touch logs/temp.txt
echo 0 > logs/value.txt

# Update and upgrade the system
sudo apt-get update
sudo apt-get upgrade -y
sudo apt install git

# Install for Respeaker mic (Kernel version should always be 5.15 or more)
git clone https://github.com/HinTak/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh

cd ..

sudo apt-get install portaudio19-dev -y

# Install pip
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
python3 -m venv audio-venv
source audio-venv/bin/activate

# Install the dependencies
pip install -r /home/pi/AudioRecordingOnBoot/requirements.txt
pip install opencv-python
sudo apt-get install libatlas-base-dev -y

deactivate

#Copy paste services and enable them
sudo cp /home/pi/AudioRecordingOnBoot/services/*.service /etc/systemd/system/
sudo systemctl enable sonaide_startup.service increment_value.service

sudo reboot
