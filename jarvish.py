import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import openai
import yt_dlp

# ✅ Set Your OpenAI API Key (Use environment variable for security)
openai.api_key = "your-api-key-here"  # Replace with a secure method

# ✅ Initialize the text-to-speech engine
engine = pyttsx3.init()

# ✅ Store user information
user_info = {
    "name": "Dhanraj Singh",
    "age": "19",
    "occupation": "Front-End Developer",
    "hobbies": "coding",
    "favorite_color": "red",
    "favorite_food": "panipuri",
    "location": "Patna"
}

def speak(text):
    """Make the assistant speak"""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greet the user based on the current time"""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak(f"Good Morning, {user_info['name']}!")
    elif 12 <= hour < 18:
        speak(f"Good Afternoon, {user_info['name']}!")
    else:
        speak(f"Good Evening, {user_info['name']}!")
    speak("How can I assist you today?")

def take_command():
    """Take voice input from the user"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.5
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {command}")
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return "None"
    except sr.RequestError:
        print("Error connecting to Google Speech Recognition API.")
        return "None"
    return command.lower()

def about_user():
    """Provide user details"""
    intro = (
        f"Your name is {user_info['name']}. You are {user_info['age']} years old and work as {user_info['occupation']}. "
        f"You enjoy {user_info['hobbies']}. Your favorite color is {user_info['favorite_color']}, "
        f"and you love eating {user_info['favorite_food']}. You live in {user_info['location']}."
    )
    speak(intro)

def chat_with_gpt(prompt):
    """Interact with OpenAI's ChatGPT"""
    try:
        client = openai.OpenAI()  # ✅ Create an OpenAI client (new format)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content
        print("ChatGPT said:", reply)
        speak(reply)
        return reply
    except openai.OpenAIError as e:
        error_msg = f"An OpenAI error occurred: {str(e)}"
        print(error_msg)
        speak(error_msg)
        return error_msg

def play_youtube_music(song_name):
    """Search and play a song from YouTube"""
    search_query = song_name + " music"
    ydl_opts = {'quiet': True, 'extract_flat': True, 'max_downloads': 1}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch:{search_query}", download=False)
        if 'entries' in result and result['entries']:
            video_url = f"https://www.youtube.com/watch?v={result['entries'][0]['id']}"
            speak(f"Playing {song_name} on YouTube")
            webbrowser.open(video_url)

def process_commands(command):
    """Process commands and respond accordingly"""
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    
    elif "who am i" in command or "tell me about myself" in command or "kuchh bol bhai" in command:
        about_user()
    
    elif "play music" in command:
        speak("What song would you like to play?")
        song_name = take_command()
        if song_name != "None":
            play_youtube_music(song_name)
    
    elif "open youtube" in command:  # ✅ Fixed indentation
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    
    elif "exit" in command or "stop" in command:
        speak("Goodbye! Have a great day.")
        return False
    
    else:
        chat_with_gpt(command)
    
    return True

def main():
    greet_user()
    while True:
        query = take_command()
        if query != "None":
            continue_processing = process_commands(query)
            if not continue_processing:
                break

if __name__ == "__main__":
    main()
