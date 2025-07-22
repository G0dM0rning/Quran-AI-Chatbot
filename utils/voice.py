from gtts import gTTS
import os

def speak_text(text):
    tts = gTTS(text)
    tts.save("response.mp3")
    os.system("start response.mp3")  # Windows
    # For macOS: os.system("afplay response.mp3")
    # For Linux: os.system("mpg321 response.mp3")
