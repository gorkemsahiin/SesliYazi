import pyaudio
import wave

class Recorder:
    def __init__(self):
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1 
        self.fs = 44100
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.recording = False 

    def start_recording(self, filename):
        self.filename = filename
        self.frames = []
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.fs,
                                  frames_per_buffer=self.chunk,
                                  input=True)

        print("Kayıt Başladı..!")
        self.recording = True  

        while self.recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def stop_recording(self):
        self.recording = False 
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(self.frames))

        print(f"Kayıt Durduruldu: {self.filename}")
