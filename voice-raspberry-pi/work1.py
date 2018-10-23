import speech_recognition as sr
import os
import tempfile
from gtts import gTTS
import time
import sys
from pygame import mixer
import paho.mqtt.client as mqtt
import json
import requests
import webbrowser as web

def get_req(path):
    req = requests.get('http://localhost:3000/{}'.format(path))
    print("HTTP Status Code: " + str(req.status_code))
    print(req.headers)
    print("content: " + req.content.decode("utf-8"))
    return req.content.decode("utf-8")


temp_data = None

mixer.init()
r= sr.Recognizer()
r.energy_threshold = 4000

def speak(sentence):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=sentence, lang='zh-tw')
        tts.save("{}.mp3".format(fp.name))
        mixer.music.load("{}.mp3".format(fp.name))
        mixer.music.play()
        time.sleep(2)

def listenTo():
    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...") 
        r.adjust_for_ambient_noise(source, duration=5)
        print("Say something!")
        audio=r.listen(source)
    try:
        my_stt = r.recognize_google(audio, language="zh-TW")
        print("you say: ", my_stt)
    except:
        print("Could not understand audio")
    return my_stt



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("KevinFan/lab305/temp_hum")

def on_message(client, userdata, msg):
    global temp_data
    if msg.topic == "KevinFan/lab305/temp_hum":
        temp_data = json.loads(msg.payload.decode("utf-8")) 
        print(temp_data['ds18b20'])
        if float(temp_data['ds18b20']['temperature']) > 30:
            speak('溫度已超過30度，現在溫度{}度'.format(temp_data['ds18b20']['temperature']))
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def watch_temp():
    client.connect("mqtt_broker", 1883, 60)
    client.loop_forever() 


speak('您需要什麼服務嗎?')
while True:
    text=listenTo()
    if (text == "請問現在溫度幾度" or text == "請問現在溫度多少" or text == "溫度多少" or text == "現在溫度" or text == "現在溫度多少" or text == "現在溫度幾度"):
        response = get_req("sensor/now/temp")
        speak("現在溫度{}度".format(response))
    elif (text == "請問現在濕度幾度" or text == "請問現在濕度多少" or text == "濕度多少" or text == "現在濕度" or text == "現在濕度多少"):
        response = get_req("sensor/now/hum")
        speak("現在濕度{}趴".format(response))
    elif (text == "監視溫度" or text == "觀察溫度"):
        watch_temp()
    elif (text == "顯示溫度清單" or text == "溫度清單" or text == "溫度列表" or text == "開啟溫度清單"):
        chromepath = "/usr/lib/chromium-browser/chromium-browser"
        web.register('chromium-browser', None, web.BackgroundBrowser(chromepath))
        web.get('chromium-browser').open_new_tab('http://localhost:3000/')
    else:
        pass

