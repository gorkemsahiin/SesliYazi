import tkinter as tk
import threading
import wave
import json
from tkinter import messagebox
from recorder import Recorder
from vosk import Model, KaldiRecognizer

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ses Kayıt Uygulaması")
        self.recorder = Recorder()
        self.recording = False

        self.start_button = tk.Button(root, text="Kaydı Başlat", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Kaydı Durdur", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.convert_button = tk.Button(root, text="Yazıya Çevir", command=self.process_audio)
        self.convert_button.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)  # Sağ alt köşeye yerleştir

        self.result_text = tk.Text(root, wrap=tk.WORD, height=10, width=50)
        self.result_text.pack(pady=10)

        self.model = Model("C:/Users/rdrc5/SesliYazi/model/vosk-model-small-tr-0.3")
        self.recognizer = KaldiRecognizer(self.model, 44100)

        self.filename = "ses_kaydi.wav"

    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        recording_thread = threading.Thread(target=self.recorder.start_recording, args=(self.filename,))
        recording_thread.start()

    def stop_recording(self):
        self.recording = False
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)

        self.recorder.stop_recording()

    def process_audio(self):
        try:
            wf = wave.open(self.filename, "rb")
        except FileNotFoundError:
            messagebox.showerror("Hata", "Kayıt dosyası bulunamadı!")
            return

        self.recognizer.SetWords(True)
        result_text = ""

        while True:
            data = wf.readframes(4000)  
            if len(data) == 0:
                break  
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                result_text += result.get('text', '') + ' '

        final_result = json.loads(self.recognizer.Result())
        result_text += final_result.get('text', '')

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)
  
  
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.geometry("400x400")  
    root.mainloop()
