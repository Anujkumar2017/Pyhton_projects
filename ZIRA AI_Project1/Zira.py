import pyttsx3
import datetime
import webbrowser
import wikipedia
import os
import speech_recognition as sr
import random

#setting voice
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty("voice",voices[0].id)

#function to speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#AI Zira wish and introduce to you
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!!")
    elif hour>=12 and hour<18:
        speak("Good Evening!!")
    else:
        speak("Good Night!!!")
    speak("I am Zira sir, Your AI desktop assistant . How may I help you?")

#this function take microphone as input and give a string as output 
def takeCommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold = 1
        audio= r.listen(source)
    try:
        print("Recognizing.....")
        # query = r.recognize_google(audio,language='en-in')
        query = r.recognize_google(audio,language='en-in')
        print(f"User said: {query}")
    except Exception as e:
        print(e)
        print("Say that again please.....")
        return "None"
    return query


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
    
        #search wikipedia 
        if "wikipedia" in query:
            speak("Searching Wikipedia....")
            query = query.replace('wikipedia','')
            results = wikipedia.summary(query,sentences=2)
            speak("According to wikipedia..")
            print(results)
            speak(results)

        #for playing music 
        elif 'play music' in query or 'play song' in query:
            music_path ='C:\\Users\\SATYA\\Desktop\\anuj\\ANUJ SONG'
            song_list =os.listdir(music_path)
            # print(song_list)
            os.startfile(os.path.join(music_path,song_list[random.randint(0,len(song_list))]))
            print("Plying music")
             
        #open google and youtube and vscode
        elif "open google" in query:
            webbrowser.open("www.google.com")
        elif 'open youtube' in query:
            webbrowser.open("www.youtube.com")
        elif 'open vs code' in query:
            os.startfile("C:\\Users\\SATYA\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
        
        #for exiting the AI 
        elif 'exit' in query:
            speak("Bye!!! See you again!!")
            exit()

