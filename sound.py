import speech_recognition as sr

# Create a Recognizer instance
recognizer = sr.Recognizer()

# Set a duration to capture the audio
with sr.Microphone() as source:
    print("Calibrating microphone...")  # Adjusts for ambient noise
    recognizer.adjust_for_ambient_noise(source, duration=1)
    
    while True:
        try:
            audio_data = recognizer.listen(source, timeout=1.5, phrase_time_limit=2)
            print("Listening to audio")
           # timeout : stops after certain time if not audio is detected
           # pharse_time_limit: how long it waits before stopping recording when it detects silence 
        except sr.WaitTimeoutError:
            print("Nothing")  # Timeout without audio input means no sound detected
