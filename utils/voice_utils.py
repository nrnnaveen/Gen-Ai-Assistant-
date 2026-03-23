import speech_recognition as sr

def record_voice():
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)

        text = recognizer.recognize_google(audio)
        return text
    except Exception:
        return None
