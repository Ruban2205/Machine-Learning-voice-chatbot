import speech_recognition as speech
import pyttsx3
import openai

# API call from .env file
with open('.env', 'r') as api: 
    key = str(api.read()).strip()

openai.api_key = key 

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

voice_recognize = speech.Recognizer()
mic = speech.Microphone()

conversation = ""
user_name = "Ruban"
bot_name = "Jerusha"

while True: 
    with mic as source: 
        print("\n Listening...")
        voice_recognize.adjust_for_ambient_noise(source, duration=0.2)
        audio = voice_recognize.listen(source)
    print("No longer listening")

    try: 
        user_input = voice_recognize.recognize_google(audio) 
    except: 
        continue

    prompt = user_name + ":" + user_input + "\n" + bot_name + ":"
    conversation += prompt

    response = openai.Completion.create(
        model="text-davinci-003", 
        prompt=conversation,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(
        user_name + ":" ,1)[0].split(bot_name + ":",1)[0]
    
    conversation += response_str + "\n"
    print(response_str)

    engine.say(response_str)
    engine.runAndWait()