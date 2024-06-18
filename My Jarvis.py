# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:16:30 2024

@author: hithy
"""
#speech recognition : converts text to speech using various APIs 
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes 
import requests, json
#for weather there's no readily available library, so it's a bit challenging, so we'll be using open weather API and create our own function to fetch weather details
#pyttsx : text to speech so that alexa can speak to us
#pywhatkit : to search on youtube(do some cool stuff)
listener = sr.Recognizer()
#engine to speak to you and initialize it
engine = pyttsx3.init()
#this gives male voice in general
#to get female voice
voices=engine.getProperty('voices')
#2nd voice among these voices and we set the id of it
engine.setProperty('voice',voices[0].id)
engine.say('Hi I am your Jarvis')
engine.say('What can I do for you')
engine.runAndWait()
def talk(text):
    engine.say(text)
    engine.runAndWait()
    
def weather(city):
    #enter your API key
    api_key="your key"
    
    #base url variable to store url
    base_url="http://api.openweathermap.org/data/2.5/weather?"
    
    city_name=city
    #complete_url variable to store complete url address
    complete_url=base_url+"appid="+api_key+"&q="+city_name
    
    #get method of requests module
    #return response object
    response=requests.get(complete_url)
    
    #json method of response object
    #convert json format data into python format data
    x=response.json()
    
    #now x contains list of nested dictionaries
    #check the value of "cod" key is not equal to "404" means city is found, otherwise city not found
    if x["cod"]!=404:
        
        #store the value of "main" key in variable y
        y=x["main"]
        
        #store the value corresponding to the "temp" key of y
        current_temperature=y["temp"]
        
        #for pressure
        current_pressure=y["pressure"]
        
        #for humidity
        current_humidity=y["humidity"]
        
        #store the value of "weather" key in variable z
        z=x["weather"]
        
        #store value corresponding to the "description" key at the 0th index of z
        weather_description=z[0]["description"]
        return str(current_temperature)
    
    

#using try block : as microphone might not work always
#microphone is source of our audio
#voice : we are listening to what is said via source calling speech recognizer
#command : voice to text using google API (we have many functions in speech recognition to convert voice to text and google api is one among them)

def take_command():
    command=""
    try:
        with sr.Microphone() as source:
            #without this we won't know when is it listening
            print('listening...')
            voice = listener.listen(source)
            command=listener.recognize_google(voice)
            command=command.lower()
            #it gets printed only if you say alexa
            if 'jarvis' in command:
                #we're removing alexa from our speech
                command=command.replace('jarvis','')
                print(command)
                #talk(command)
            #to debug if it is working or not, print it
            #so whenever an exception is thrown python ignores it as we passed it simply
    except:
        pass
    return command
#so take command takes command we give and returns it
#here we are converting our speech to text and then making alexa speak it out
#runnig alexa will take the command and we process it
def run_alexa():
    flag=1
    while flag:
        command=take_command()
        if 'play' in command:
            song=command.replace('play','')
            talk('playing'+song)
            pywhatkit.playonyt(song)
        elif 'time' in command:  
            #24hr time in string format
            #time=datetime.datetime.nom().strftime('%H:%M:%S')
            #12 hr time
            #to get AM PM %p
            time=datetime.datetime.now().strftime('%I:%M %p')
            print('current time is'+time)
            talk('cuurent time is'+time)
        elif 'who is' in command:
            person=command.replace('who is','')
            #1 line about the person asked from wikipedia
            info=wikipedia.summary(person,1)
            print(info)
            talk(info)
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        elif 'weather' in command:
            talk('please tell the city')
            city=take_command()
            weather_api=weather('Patna')
            talk(weather_api+'degree fahreneit')
        elif 'thank you' in command:
            talk('my pleasure')
        elif 'stop' in command:
            flag=0
            #we can use sys library and sys.exit() command
        else:
            talk('please say the command again')


run_alexa()
    
  
    