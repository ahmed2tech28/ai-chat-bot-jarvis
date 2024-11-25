import google.generativeai as genai
from config import *
import os
import speech_recognition as sr

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def speak(text: str):
    os.system(f"say \"{text}\"")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"Command received: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            speak("Sorry, I could not understand. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
            speak("There was an error with the speech recognition service.")
            return None

def generate_response(command: str):
    response = model.generate_content(command)
    return response.text

def adjust_response_for_pronunciation(response: str):
    adjusted_lines = []
    lines = response.split("\n")
    for line in lines:
        line = line.strip()
        if line:
            line = line.replace("OOP", "Object-Oriented Programming")
            line = line.replace("e.g.", "for example")
            adjusted_lines.append(line)
    return adjusted_lines

if __name__ == "__main__":
    command = take_command()
    response = generate_response(command)
    
    adjusted_lines = adjust_response_for_pronunciation(response)
    for line in adjusted_lines:
        print(line)
        speak(line)
