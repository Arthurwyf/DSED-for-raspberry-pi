import sounddevice as sd
from scipy.io.wavfile import write
import time
from datetime import datetime

time.sleep(30)

freq = 44100

duration = 60

with open('/home/pi/logs/value.txt') as file:
	value = file.readline().strip()

sd.default.device = 'seeed-2mic-voicecard'

while True:
	recording = sd.rec(int(duration * freq), samplerate = freq, channels = 1)
	sd.wait()
	now = datetime.now()
	write('/home/pi/records/recording_{}_{}.wav'.format(now.strftime("%d-%m-%YT%H%M%S"), value), freq, recording)

