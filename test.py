import urllib.request
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import time

# Jedna sekunda do 1024 * 95 bajtów
CHUNK = 1024 * 10
# poziom głośności od którego będzie program informował o hałasie
silence_limit = 20000

audio = pyaudio.PyAudio()
u = urllib.request.urlopen("http://192.168.8.107:8080/audio.wav")

arr = u.read(44)

# stream = audio.open(format=pyaudio.paFloat32,
#                 channels=1,
#                 rate=44100,
#                 output=True)
# wf = wave.open("D:\\Workspace\\python\\rpo-smartphone\\file.wav", 'rb')
stream = audio.open(format = pyaudio.paInt16,
                channels =int.from_bytes(arr[22:24], byteorder="little"),
                rate = int.from_bytes(arr[24:28], byteorder="little"),
                output=True)
                
print("Rozpoczęto nasłuchiwanie...")

data = u.read(CHUNK)

plt.figure(1)
plt.title("Signal Wave...")

start = time.time()
arr = np.asarray([])

while time.time() < start + 10:
    stream.write(data)
    data = u.read(CHUNK)
    data_np = np.asarray(data)
    arr = np.append(arr, data_np)
    data_np = np.frombuffer(data_np, dtype=np.int16)
    if np.any(data_np > silence_limit):
        print("Wykryto hałas!")

wav_r = np.frombuffer(arr, dtype=np.int16)
plt.plot(wav_r)

plt.show()



stream.close()
audio.terminate()