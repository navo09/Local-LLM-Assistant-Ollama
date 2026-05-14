import speech_recognition as sr
import webbrowser
import requests
from gtts import gTTS
import pygame
import os
import pyttsx3
from deep_translator import GoogleTranslator
import musicLibrary
import json
import time
import ollama
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from datetime import datetime
#for lattest info



NEWS_API_KEY = "your news api"


def get_latest_info(query):
    try:
        with DDGS() as ddgs:
            # সার্চ রেজাল্ট থেকে কন্টেন্ট নেওয়া
            results = [r for r in ddgs.text(f"{query} 2026", max_results=3)]
            
        web_context = ""
        for r in results:
            web_context += f"Title: {r['title']}\nSnippet: {r['body']}\n\n"
            
        return web_context if web_context else "No live info found."
    except Exception as e:
        return f"Search error: {e}"

recognizer = sr.Recognizer()

def speak(text):
    print(f"ATX Speaking: {text}")
    engine = pyttsx3.init()
    engine.setProperty('rate', 175) 
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def speak_bangla(text):
    try:
        tts = gTTS(text=text, lang='bn')
        tts.save("news.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("news.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.quit()
        if os.path.exists("news.mp3"):
            os.remove("news.mp3")
    except Exception as e:
        print(f"Bangla Speak Error: {e}")

def aiProcess(command):
    try:
        # ১. অটোমেটিক আজকের তারিখ এবং সময় বের করা
        # আজ ১৪ মে, ২০২৬ - এটি সিস্টেম থেকে অটো নিবে
        now = datetime.now()
        current_date = now.strftime("%A, %B %d, %Y")
        current_time = now.strftime("%H:%M:%S")

        # ২. ডিসিশন মেকিং (Router Logic)
        # এখানে আমরা llama3 ব্যবহার করছি কারণ ওর রিজনিনিং পাওয়ার ৩বি-র চেয়ে অনেক বেশি
        router_prompt = f"""
        Today is {current_date}, Time: {current_time}.
        User Query: "{command}"
        
        Task: 
        As an AI controller, decide if this query needs real-time data from the web (Search) 
        to be answered accurately according to the current date ({current_date}).
        
        - Respond ONLY with "SEARCH_REQUIRED" if the query is about news, 2026 events, current world leaders, or weather.
        - Respond ONLY with "INTERNAL_KNOWLEDGE" if the query is about coding, logic, general science, or something you already know.
        """
        
        # সিদ্ধান্ত নেওয়ার জন্য llama3 কল করা
        decision = ollama.chat(
            model='llama3', 
            messages=[{"role": "user", "content": router_prompt}]
        )
        decision_text = decision['message']['content'].strip().upper()

        context = ""
        # ৩. যদি সার্চের প্রয়োজন হয় (DuckDuckGo Search Function কল হবে)
        if "SEARCH_REQUIRED" in decision_text:
            print(f"Novo (7B): Detected need for live data for {current_date}. Searching...")
            context = get_latest_info(command) # তোর আগের সেই সার্চ ফাংশন
        else:
            print(f"Novo (7B): Processing with internal intelligence at {current_time}...")

        # ৪. ফাইনাল রেসপন্স জেনারেশন (পারসোনা + কনটেক্সট)
        # এখানে qwen2.5:7b ব্যবহার করা যেতে পারে কারণ ওটা বেশ ফাস্ট এবং বুদ্ধিমান
        system_instruction = f"""
        You are 'Novo', a high-intelligence AI assistant and mentor for Amit Navojit.
        Navojit is a CSE student at Daffodil International University (DIU) with a dream of opening an IT firm.
        
        Current Status:
        - Date: {current_date}
        - Time: {current_time}
        - Search Results: {context if context else 'No live search needed for this query.'}
        
        Instructions:
        1. Use the Search Results to answer facts about 2026 or current events.
        2. Always be professional, insightful, and supportive of Navojit's career goals.
        3. If no search data is found, answer based on your best logical intelligence but mention today's date.
        """

        response = ollama.chat(
            model='qwen2.5:7b', # তুই চাইলে এখানেও llama3 ব্যবহার করতে পারিস
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": command}
            ]
        )
        
        return response['message']['content']

    except Exception as e:
        # কোনো কারণে এরর হলে সেটা টার্মিনালে দেখাবে
        return f"Error in Novo's Brain (7B Process): {e}"

# ব্যবহার করার নিয়ম:
# print(aiProcess("Who is the current prime minister of India?"))
    
def processCommand(c):
    c_lower = c.lower().strip()
    
    if "open google" in c_lower:
        webbrowser.open("https://google.com")
    elif "open facebook" in c_lower:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c_lower:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    
    elif c_lower.startswith("play"):
        song = c_lower.split(" ")[1]
        if song in musicLibrary.music:
            webbrowser.open(musicLibrary.music[song])
        else:
            speak("Song not found.")

    elif "news in bangla" in c_lower:
        r = requests.get(f"https://newsapi.org/v2/everything?q=bangladesh&sortBy=publishedAt&apiKey={NEWS_API_KEY}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            speak("Reading news in Bengali.")
            for article in articles[:3]:
                title = article['title']
                translated = GoogleTranslator(source='auto', target='bn').translate(title)
                print(f"Bengali News: {translated}")
                speak_bangla(translated)

    elif "news in english" in c_lower:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            speak("Here are the top headlines.")
            for article in articles[:5]:
                title = article.get("title")
                if title:
                    speak(title)
        else:
            speak("Failed to fetch news.")

    else:
      output = aiProcess(c)
    print(f"\nAI Response: {output}")

    if output:
        is_bangla = any('\u0980' <= char <= '\u09FF' for char in output)
        if is_bangla:
            speak_bangla(output)
        else:
            speak(output)
if __name__ == "__main__":
    speak("ATX is online.")

    
while True:
    try:
        print("\n1. Say 'ATX' | 2. Type Command | 'exit' to quit")

        choice = input("Choose (voice/type): ").lower()

        # 🔊 Voice mode
        if choice == "voice":
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                word = recognizer.recognize_google(audio)

            if word.lower() == "ATX":
                speak("Yes Boss?")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)

        # ⌨️ Text mode (SAFE)
        else:
            user_input = input("Type command: ")

            if user_input.lower() == "exit":
                speak("Goodbye Boss!")
                break

            if user_input.strip():
                processCommand(user_input)

    except Exception as e:
        print(f"Error: {e}")