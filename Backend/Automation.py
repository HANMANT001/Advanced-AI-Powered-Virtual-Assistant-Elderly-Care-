import os
import subprocess
import webbrowser
import keyboard
import requests
import asyncio
from typing import cast
from groq import Groq
from bs4 import BeautifulSoup
from pynput.keyboard import Key, Controller
from dotenv import dotenv_values
from datetime import datetime
from pynput import keyboard as pk
from playsound import playsound
import sys
from win32com.client import Dispatch
from AppOpener import open as appopen, close as appclose
import random
import time
from pywhatkit import playonyt, search
import webbrowser

# Global variables for chatbot context and session management.
ChatHistory = []
messages = []

# Assuming env variables are loaded elsewhere or will be added.
# For now, let's mock a simple system for demonstration.
os.environ['Username'] = 'YourUsername'
os.environ['Assistantname'] = 'YourAssistant'
GroqAPIKey = 'YOUR_GROQ_API_KEY' # Replace with your actual key

# Initialize the Groq client
client = Groq(api_key=GroqAPIKey)

SystemChatBot = [
    {"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, articles etc."}
]

# Function to perform a Google search.
def GoogleSearch(Topic):
    search(Topic) # Use pywhatkit's search function to perform a Google search.
    return True # Indicate success.

# Function to generate content using AI and save it to a file.
def Content(Topic):
    # Nested function to open a file in Notepad.
    def OpenNotepad(file):
        default_text_editor = "notepad.exe" # Default text editor.
        subprocess.Popen([default_text_editor, file]) # Open the file in Notepad.

    # Nested function to generate content using the AI chatbot.
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"}) # Add the user's prompt to messages.

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768", # Specify the AI model.
            messages=SystemChatBot + messages, # Include system instructions and chat history.
            max_tokens=2048, # Limit the maximum tokens in the response.
            temperature=0.7, # Adjust response randomness.
            top_p=1, # Use nucleus sampling to control diversity.
            stream=True, # Enable streaming response.
            stop=None # Allow the model to determine stopping conditions.
        )
        
        Answer = "" # Initialize an empty string for the response.

        # Process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content: # Check for content in the current chunk.
                Answer += chunk.choices[0].delta.content # Append the content to the answer.

        Answer = Answer.replace("</s>", "") # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer}) # Add the AI's response to messages.
        return Answer

    Topic: str = Topic.replace("content", "") # Remove "content" from the topic.
    ContentByAI = ContentWriterAI(Topic) # Generate content using AI.

    # Save the generated content to a text file.
    with open(f"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI) # Write the content to the file.

    OpenNotepad(f"Data\{Topic.lower().replace(' ', '')}.txt") # Open the file in Notepad.
    return True # Indicate success.

# Function to search for a topic on YouTube.
def YouTubeSearch(Topic):
    Url4search = f"https://www.youtube.com/results?search_query={Topic}" # Construct the YouTube search URL.
    webbrowser.open(Url4search) # Open the search URL in a web browser.
    return True # Indicate success.

# Function to play a video on YouTube.
def PlayYouTube(query):
    playonyt(query) # Use pywhatkit's playonyt function to play the video.
    return True # Indicate success.

# Function to open an application or a relevant webpage.
def OpenApp(app, sess, requests):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True) # Attempt to open the app.
        return True # Indicate success.
    except:
        # Nested function to extract links from HTML content.
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, "html.parser") # Parse the HTML content.
            links = soup.find_all('a', jsname='UNcKbd') # Find relevant links.
            return [link.get('href') for link in links] # Return the links.

        # Nested function to perform a Google search and retrieve HTML.
        def search_google(query):
            url = f"https://www.google.com/search?q={query}" # Construct the Google search URL.
            headers = {"User-Agent": "Moozila/5.0"} # Use the predefined user-agent.
            response = sess.get(url, headers=headers) # Perform the GET request.

            if response.status_code == 200:
                return response.text # Return the HTML content.
            else:
                print("Failed to retrieve search results.") # Print an error message.
                return None

        html = search_google(app) # Perform the Google search.
        if html:
            link = extract_links(html)[0] # Extract the first link from the search results.
            webbrowser.open(link) # Open the link in a web browser.
            return True # Indicate success.
        return False # Indicate failure.

# Function to close an application.
def CloseApp(app):
    if "chrome" in app:
        pass # Skip if the app is Chrome.
    try:
        appclose(app, match_closest=True, output=True, throw_error=True) # Attempt to close the app.
        return True # Indicate success.
    except:
        return False # Indicate failure.

# Function to execute system-level commands.
def System(command):
    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release('volume mute') # Simulate the mute key press.

    # Nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release('volume mute') # Simulate the unmute key press.

    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release('volume up') # Simulate the volume up key press.

    # Nested function to decrease the system volume.
    def volume_down():
        keyboard.press_and_release('volume down') # Simulate the volume down key press.

    # Execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True # Indicate success.

# Asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):
    funcs = [] # List to store asynchronous tasks.

    with requests.Session() as sess: # Use a session for requests.
        for command in commands:
            if command.startswith("open "): # Handle "open" commands.
                if "open it" in command:
                    pass # Ignore "open it" commands.
                if "open file" == command:
                    pass # Ignore "open file" commands.
                else:
                    fun = asyncio.to_thread(OpenApp, command.removeprefix("open "), sess, requests) # Schedule app opening.
                    funcs.append(fun)

            elif command.startswith("general "): # Placeholder for general commands.
                pass

            elif command.startswith("realtime "): # Placeholder for real time commands.
                pass

            elif command.startswith("close "): # Handle "close" commands.
                fun = asyncio.to_thread(CloseApp, command.removeprefix("close ")) # Schedule app closing.
                funcs.append(fun)

            elif command.startswith("play"): # Handle "play" commands.
                fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play ")) # Schedule YouTube playback.
                funcs.append(fun)

            elif command.startswith("content "): # Handle "content" commands.
                fun = asyncio.to_thread(Content, command.removeprefix("content ")) # Schedule content creation.
                funcs.append(fun)

            elif command.startswith("google search"): # Handle Google search commands.
                fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")) # Schedule Google search.
                funcs.append(fun)

            elif command.startswith("youtube search"): # Handle YouTube search commands.
                fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")) # Schedule YouTube search.
                funcs.append(fun)

            elif command.startswith("system "): # Handle system commands.
                fun = asyncio.to_thread(System, command.removeprefix("system ")) # Schedule system command.
                funcs.append(fun)

            else:
                print("No Function Found. For command: ", command) # Print an error for unrecognized commands.

    results = await asyncio.gather(*funcs, return_exceptions=True) # Execute all tasks concurrently.

    for result in results: # Process the results.
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynchronous function to automate command execution.
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands): # Translate and execute commands.
        pass
    return True # Indicate success.