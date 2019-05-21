"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import sys
import os

CHUNK = 1024
WAVE_INPUT_FILENAME = "test.wav"

if not os.path.exists(WAVE_INPUT_FILENAME):
    print("Plays a wave file.\nUsage: %s filename.wav" % WAVE_INPUT_FILENAME)
    sys.exit(-1)

wf = wave.open(WAVE_INPUT_FILENAME, 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while data:
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()
p.terminate()

wf.close()
