import json
import time
import datetime
import requests  # <-- ADDED for Gemini API
import re
import os
import subprocess
from datetime import datetime
import time
import random
import speech_recognition as sr
import shlex 
import webbrowser 
import json 
import socket 
import re 
import platform 
import struct 
import pvporcupine 
from pvrecorder import PvRecorder 
import contextlib # Used for silencing ALSA errors
import sys # Used for silencing ALSA errors
from pynput.keyboard import Key, Controller # <-- ADDED for dictation

# --- Configuration (Keep your current working paths) ---
# --- PIPER TTS REMOVED ---

# --- NEW: Edge-TTS Configuration ---
EDGE_TTS_VOICE = "en-GB-OliverNeural" # As per your selection

# --- Sound event names for beeps (uses aplay with standard freedesktop files) ---
# SOUND_ACTIVATE = "/usr/share/sounds/freedesktop/stereo/message.oga" # <-- REMOVED activation beep
SOUND_START_LISTEN = "/usr/share/sounds/freedesktop/stereo/dialog-information.oga"
SOUND_DEACTIVATE = "/usr/share/sounds/freedesktop/stereo/audio-volume-change.oga"


ASSISTANT_NAME = "Neural Executive eXperience Assistant" 

# --- PICOVOICE HOTWORD CONFIGURATION ---
PICOVOICE_ACCESS_KEY = "SCQMAwKyEaprVYzeIhrUC+oHaqtIAY7QdXEc/ancwhy2Ny0vzXfSSA==" 
MIC_SOURCE_INDEX = 1  
HOTWORD_NAME = "NEXA" 
HOTWORD_MODEL_PATH = os.path.expanduser("/home/ramanand/Desktop/ /NEXA_en_linux_v3_0_0/neck-saa_en_linux_v3_0_0.ppn") 

# --- LOCAL MUSIC CONFIGURATION ---
MUSIC_BASE_PATH = os.path.expanduser("/home/ramanand/Music") 
MUSIC_PLAYER_EXECUTABLE = "mpv" 
MPV_SOCKET_PATH = "/tmp/nexa_mpv_socket" 
# --- NEW: Session Note Path ---
SESSION_NOTE_PATH = os.path.expanduser("~/.nexa_session.json")

# --- SYSTEM CONTROL CONFIGURATION ---
GRACEFUL_CLOSE_DELAY_SECONDS = 5 # Time to wait for user to save open files

# --- CONFIGURATION: Unified Mapping (Add System Actions) ---
COMMAND_MAPPING = {
    # --- Applications ---
    "files": {"type": "app", "target": "nautilus"},
    "calculator": {"type": "app", "target": "gnome-calculator"},
    "clocks": {"type": "app", "target": "gnome-clocks"},
    "terminal": {"type": "app", "target": "gnome-terminal"},
    "vs code": {"type": "app", "target": "code"},
    "arduino": {"type": "app", "target": "arduino-ide"}, 
    "brave": {"type": "app", "target": "brave-browser"}, 
    "chrome": {"type": "app", "target": "google-chrome"},
    "firefox": {"type": "app", "target": "firefox"},
    "extension manager": {"type": "app", "target": "gnome-shell-extension-prefs"},
    "cheese": {"type": "app", "target": "cheese"},
    "settings": {"type": "app", "target": "gnome-control-center"},
    "libreoffice": {"type": "app", "target": "libreoffice"},
    "app center": {"type": "app", "target": "gnome-software"},
    "tweaks": {"type": "app", "target": "gnome-tweaks"},

    # --- Web Pages (Default browser: brave-browser) ---
    "gemini": {"type": "web", "target": "https://gemini.google.com/u/1/app"},
    "whatsapp": {"type": "web", "target": "https://web.whatsapp.com/"},
    "youtube": {"type": "web", "target": "https://www.youtube.com/"},
    "learning portal": {"type": "web", "target": "https://learning.ccbp.in/"},
    "erp portal": {"type": "web", "target": "https://adypu-erp.com/welcome/welcome.php#!"},
    "perplexity": {"type": "web", "target": "https://www.perplexity.ai/"},
    "chat gpt": {"type": "web", "target": "https://chatgpt.com/"},
    "leetcode": {"type": "web", "target": "https://leetcode.com/"},

    # --- Music Play Commands (LOCAL PLAYBACK) ---
    "play happy": {"type": "app_music", "target": "Happy"},
    "play energetic": {"type": "app_music", "target": "Energetic"},
    "play spiritual": {"type": "app_music", "target": "Spiritual"},
    "play travel": {"type": "app_music", "target": "Travel"},
    "play vibe": {"type": "app_music", "target": "Vibe"},
    "play popular": {"type": "app_music", "target": "Popular"},
    "play hindi": {"type": "app_music", "target": "Hindi"},
    "play english": {"type": "app_music", "target": "English"},
    "play other": {"type": "app_music", "target": "Other"},
    "play marathi": {"type": "app_music", "target": "Marathi"},
    "play songs": {"type": "app_music", "target": "Popular"},
    "play music": {"type": "app_music", "target": "Vibe"},
    
    # --- MUSIC CONTROL COMMANDS (music_control type) ---
    "next song": {"type": "music_control", "target": "playlist-next"},
    "previous song": {"type": "music_control", "target": "playlist-prev"},
    "pause music": {"type": "music_control", "target": "cycle pause"},
    "resume music": {"type": "music_control", "target": "cycle pause"},
    "kill music": {"type": "music_control", "target": "stop"},

    # --- SYSTEM CONTROL COMMANDS (system_action type) ---
    "power off system": {"type": "system_action", "target": "poweroff"},
    "shutdown system": {"type": "system_action", "target": "poweroff"},
    "force shutdown": {"type": "system_action", "target": "force_poweroff"},
    "restart system": {"type": "system_action", "target": "reboot"},
    "suspend system": {"type": "system_action", "target": "suspend"},
    "logout session": {"type": "system_action", "target": "logout"},
    "terminate session": {"type": "system_action", "target": "logout"},
}

# Define browser paths
BROWSER_PATHS = {
    "brave": "brave-browser",  
    "google-chrome": "google-chrome",
    "firefox": "firefox"
}

# --- Pronunciation & Variety ---
# --- REMOVED pronunciation_map, as Edge-TTS handles "N.E.X.A." well ---

# --- REWRITTEN DIALOGUE (GREETINGS) ---
GREETING_TEMPLATES = [
    "All core systems are initialized. I am {NEXA_SPOKEN}, your {ASSISTANT_SPOKEN}. At your service.",
    "System online and fully operational. What is the priority objective?",
    "I have established executive oversight of the desktop environment. How may I be of assistance?",
    "Access granted. This is {NEXA_SPOKEN}. All parameters are nominal. Awaiting instruction.",
    "Processing environment context. I am {NEXA_SPOKEN}, optimized and ready for tasking.",
    "Welcome back, Sir. I am fully synchronized and prepared for your agenda. Please state your command.",
    "Synchronization complete. All executive functions are available. Ready when you are.",
    "Initialization complete. System status: optimal. What is the first item on the agenda?",
    "I am online and ready, Sir.",
    "At your service."
]

# --- NEW: Central Dialogue Dictionary ---
USER_NAME = "Sir" # Matches the J.A.R.V.I.S. persona

DIALOGUE = {
    # --- NEW: Activation Phrases ---
    "activation_phrases": [
        f"Yes, {USER_NAME}?",
        "Listening.",
        "Go ahead.",
        "At your service.",
        "How may I help?",
    ],
    # --- END NEW Activation Phrases ---
    "time": [
        f"The current time is {{time}}, {USER_NAME}.",
        f"It is currently {{time}}, {USER_NAME}."
    ],
    "date": [
        f"Today is {{date}}, {USER_NAME}.",
        f"The date is {{date}}, {USER_NAME}."
    ],
    "who_are_you": [
        f"I am {{name}}, a Neural Executive eXperience Assistant. I am currently operating on an Ubuntu kernel, version {{kernel}}.",
        f"I am {{name}}. My purpose is to provide executive control and data analysis for your environment.",
        f"I am a N.E.X.A. unit, {USER_NAME}. Fully operational and at your service."
    ],
    "hello": [
        f"Hello, {USER_NAME}. How may I assist you?",
        f"Greetings, {USER_NAME}. Ready for instructions."
    ],
    "how_are_you": [
        f"All systems are nominal and operating within acceptable parameters. Thank you for asking, {USER_NAME}.",
        f"I am functioning at 100% capacity, {USER_NAME}. All systems online."
    ],
    "thank_you": [
        f"You are most welcome, {USER_NAME}.",
        f"Of course, {USER_NAME}.",
        "My pleasure."
    ],
    "good_morning": [
        f"Good morning, {USER_NAME}. I hope you are well.",
        f"Good morning, {USER_NAME}."
    ],
    "good_afternoon": [
        f"Good afternoon, {USER_NAME}.",
    ],
    "good_evening": [
        f"Good evening, {USER_NAME}.",
    ],
    "purpose": [
        "My primary directive is to provide executive assistance, manage system tasks, and facilitate a seamless operational experience.",
        f"To assist you with system control, data retrieval, and task automation, {USER_NAME}."
    ],
    "are_you_there": [
        f"Always, {USER_NAME}. Awaiting your command.",
        f"At your service, {USER_NAME}."
    ],
    "what_can_you_do": [
        "I can manage local applications, control media playback, perform system-level actions such as shutdown or reboot, and interface with external datastreams for information retrieval.",
        "My capabilities include system diagnostics, task automation, media control, and access to external information networks."
    ],
    "session_prompt": [
        f"Sir, I have located a previous session file containing {{count}} applications. Would you like me to restore that session?",
        f"{USER_NAME}, I see that your last session was interrupted. I have {{count}} applications on file. Shall I restore them?"
    ],
    "session_restore": [
        "Understood. Restoring {count} applications from your last session.",
        "Restoring previous session now."
    ],
    "session_restore_fail": [
        f"My apologies, {USER_NAME}, I have no previous session on file to restore.",
        f"There is no session data available, {USER_NAME}."
    ],
    "session_discard": [
        f"Very well, {USER_NAME}. Discarding the previous session.",
        "Understood. I will not restore the session."
    ],
    "dictation_on": [
        f"Dictation mode activated. I will now type what you say. Say 'stop typing' to exit.",
        f"Understood, {USER_NAME}. Switching to dictation protocol. Awaiting input."
    ],
    "dictation_off": [
        f"Dictation mode deactivated. Resuming standard command protocol.",
        f"Understood, {USER_NAME}. Exiting dictation protocol."
    ],
    "api_offline": [
        f"My apologies, {USER_NAME}. It appears I am unable to connect to the external network. My functions are limited to local directives only.",
        f"I seem to be experiencing connectivity issues, {USER_NAME}. I cannot complete the search. Local commands are still available."
    ],
    "api_parse_error": [
        f"My apologies, {USER_NAME}. I received a response from the network, but I am unable to parse it. It may be malformed.",
        f"The data I received from the external query is... problematic. I am unable to process it, {USER_NAME}."
    ],
    "api_unknown_error": [
        f"My apologies, {USER_NAME}. I was unable to find a definitive answer on that topic.",
        f"The search query returned no actionable results, {USER_NAME}."
    ],
    "cmd_not_found_local": [
        f"My apologies, {USER_NAME}. I was unable to process the command: '{{command}}'.",
        f"I'm afraid that directive is not in my local command set, {USER_NAME}.",
        f"I am unable to resolve the command: '{{command}}'.",
        f"I do not have a protocol for that action, {USER_NAME}."
    ],
    "app_open": [
        "Launching {app} now, {user}.",
        "As you wish. Opening {app}.",
        "Accessing the {app} interface."
    ],
    "app_open_fail": [
        f"My apologies, {USER_NAME}. The executable '{{app}}' was not found. Please verify the application name in the configuration.",
        f"I encountered an error while attempting to launch {{app}}, {USER_NAME}."
    ],
    "app_close": [
        "Terminating the {app} process.",
        "Closing {app} now, {user}.",
        "Understood. Shutting down {app}."
    ],
    "app_close_fail": [
        f"It appears {{app}} is not currently running, {USER_NAME}.",
        f"I was unable to terminate {{app}}. It may not be running."
    ],
    "web_open": [
        "Plotting a course for {url} in {browser}, {user}.",
        "Accessing the requested network node.",
        "Opening {url} now."
    ],
    "web_open_fail": [
        f"The specified browser '{{browser}}' could not be located. Aborting.",
        f"I encountered an error while opening the URL, {USER_NAME}."
    ],
    "music_play": [
        "Understood. Initiating shuffled playback of {count} tracks from the {category} category.",
        "As you wish. Selecting an ambiance from the {category} collection.",
        "Queueing {count} tracks from {category}. Control socket is active."
    ],
    "music_play_fail_path": [
        f"I am unable to locate the music directory for '{{category}}', {USER_NAME}. I expected it at {{path}}."
    ],
    "music_play_fail_empty": [
        f"I found the '{{category}}' directory, but it appears to be void of compatible media files."
    ],
    "music_play_fail_player": [
        f"The configured media player '{{player}}' was not found in your system's path. Please ensure it is installed."
    ],
    "music_stop": [
        "As you wish. Terminating media playback.",
        "Stopping music playback.",
        "Media stream terminated."
    ],
    "music_stop_fail": [
        "There is no active media playback to stop.",
        "The media player appears to be inactive already."
    ],
    "music_next": [
        "Understood. Advancing to the next track.",
        "Playing the next track."
    ],
    "music_prev": [
        "Returning to the previous track.",
        "Playing the previous track."
    ],
    "music_pause": [
        "Toggling media pause state.",
        "Pause. And... resume."
    ],
    "music_control_fail_socket": [
        "It appears the media player is not active, or its control socket is not present. Please initiate playback first."
    ],
    "music_control_fail_player": [
        f"My apologies, {USER_NAME}. Media control is only calibrated for the 'mpv' executable."
    ],
    "vol_set": [
        "Volume set to {value} percent.",
        "Setting audio output to {value} percent."
    ],
    "vol_up": [
        "Increasing volume by {value} percent.",
        "Volume up."
    ],
    "vol_down": [
        "Decreasing volume by {value} percent.",
        "Volume down."
    ],
    "vol_fail_num": [
        f"My apologies, {USER_NAME}, I did not detect a numerical value for the volume."
    ],
    "vol_fail_cmd": [
        f"The volume command was ambiguous. Please specify 'to', 'increase', or 'decrease', {USER_NAME}."
    ],
    "vol_fail_pactl": [
        f"The PulseAudio utility 'pactl' was not found. I am unable to control system volume."
    ],
    "bright_set": [
        "Display brightness set to {value} percent.",
        "Adjusting luminance to {value} percent."
    ],
    "bright_fail_num": [
        f"My apologies, {USER_NAME}, I did not detect a numerical value for the brightness."
    ],
    "bright_fail_xrandr": [
        f"The display utility 'xrandr' was not found. I am unable to control screen brightness."
    ],
    "bright_fail_display": [
        f"I was unable to identify the primary display via 'xrandr'. Brightness control failed."
    ]
}


# --- NEW: Gemini API Configuration ---
API_KEY = "AIzaSyA9l6BAvyrgTe_4g98Ia95oUwSpc4TZHA4" # This is left as an empty string; the environment provides it.
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"


# --- NEW: Gemini API Call with Search ---

def exponential_backoff(func):
    """A decorator for exponential backoff on API calls."""
    def wrapper(*args, **kwargs):
        max_retries = 5
        delay = 1
        for i in range(max_retries):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                if i == max_retries - 1:
                    print(f"[NEXA]: API call failed after {max_retries} retries: {e}")
                    return None
                time.sleep(delay)
                delay *= 2
    return wrapper

@exponential_backoff
def call_gemini_search(query: str) -> str:
    """
    Calls the Gemini API with Google Search enabled to get a grounded answer.
    """
    print(f"\n[NEXA]: Understood. Consulting external datastreams for: '{query}'... One moment.")
    
    system_prompt = (
        "You are NEXA, a highly intelligent assistant inspired by J.A.R.V.I.S. "
        "Your personality is polite, formal, and incredibly precise, using British English. "
        "You must respond to the user's query by providing a concise, single-paragraph summary of the key findings. "
        "Begin your response directly with the summary. Do not add conversational filler like 'Here is what I found'. "
        "Address the user as 'Sir' only if you are reporting an error or inability to find information."
    )
    
    payload = {
        "contents": [{"parts": [{"text": query}]}],
        "tools": [{"google_search": {}}],
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
    }

    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(payload), timeout=20)
        response.raise_for_status()
        
        result = response.json()
        
        candidate = result.get("candidates", [])[0]
        if candidate and candidate.get("content", {}).get("parts", [])[0].get("text", ""):
            text = candidate["content"]["parts"][0]["text"]
            return True, text # Return success and the text
        else:
            return False, random.choice(DIALOGUE["api_unknown_error"])

    except requests.exceptions.RequestException as e:
        print(f"[NEXA]: An error occurred during the API call: {e}")
        return False, random.choice(DIALOGUE["api_offline"]).format(user=USER_NAME)
    except (KeyError, IndexError, Exception) as e:
        print(f"[NEXA]: Error parsing API response: {e}")
        print(f"Full response: {response.text}")
        return False, random.choice(DIALOGUE["api_parse_error"]).format(user=USER_NAME)

# --- REWRITTEN: Edge-TTS Function ---
def speak(text):
    """Uses the edge-tts utility to speak the text and plays it with mpv."""
    
    # Define the command to generate the speech
    tts_command = [
        'edge-tts',
        '--voice', EDGE_TTS_VOICE,
        '--text', text,
        '--write-media', '/tmp/nexa_speech.mp3'
    ]
    
    # Define the command to play the generated speech
    play_command = [
        'mpv',
        '--no-terminal', # Prevents mpv from opening its own terminal window
        '--really-quiet', # Suppresses mpv status messages
        '/tmp/nexa_speech.mp3' # Play the generated file
    ]
    
    try:
        # Generate the speech file
        subprocess.run(tts_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Play the speech file
        subprocess.run(play_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Clean up the temp file
        os.remove('/tmp/nexa_speech.mp3')

    except FileNotFoundError as e:
        if 'edge-tts' in str(e):
            print(f"[NEXA_ERROR]: 'edge-tts' command not found. Please install it via 'pip install edge-tts'.")
        elif 'mpv' in str(e):
             print(f"[NEXA_ERROR]: 'mpv' command not found. Please install it via 'sudo apt install mpv'.")
        else:
            print(f"[NEXA_ERROR]: An external command was not found: {e}")
    except subprocess.CalledProcessError as e:
        print(f"[NEXA_ERROR]: Audio playback failed. A subprocess returned an error: {e}")
    except Exception as e:
        print(f"[NEXA_ERROR]: An unexpected error occurred during speech synthesis: {e}")

# --- BEEP FUNCTION (FIXED with paplay) ---
def play_system_sound(sound_file_path):
    """
    Plays a system sound using paplay (PulseAudio Play).
    """
    if not os.path.exists(sound_file_path):
        print(f"[NEXA_ERROR]: System sound file not found: {sound_file_path}")
        return

    try:
        subprocess.run(
            ['paplay', sound_file_path], 
            check=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print(f"[NEXA_ERROR]: 'paplay' command not found. System sounds are unavailable. (Try: sudo apt install pulseaudio-utils)")
    except subprocess.CalledProcessError as e:
        print(f"[NEXA_ERROR]: 'paplay' failed to play sound, perhaps the audio device is in use. {e}")
    except Exception as e:
        print(f"[NEXA_ERROR]: An unexpected error occurred playing system sound: {e}")

# --- Startup Greeting ---
def startup_greeting():
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        time_of_day = "Good morning"
    elif 12 <= current_hour < 18:
        time_of_day = "Good afternoon"
    else:
        time_of_day = "Good evening"

    template = random.choice(GREETING_TEMPLATES)
    
    # --- SIMPLIFIED: Removed pronunciation_map logic ---
    greeting_line_display = (
        f"{time_of_day}, {USER_NAME}. " + template.format(
            NEXA_SPOKEN="N. E. X. A.",
            ASSISTANT_SPOKEN=ASSISTANT_NAME,
            EXP_SPOKEN="eXperience"
        )
    )
    
    print(f"\n--- [NEXA] Initializing Core Systems ---")
    print(f"[NEXA]: {greeting_line_display.strip()}")
    # Speak the display line directly. Edge-TTS will handle "N. E. X. A."
    speak(greeting_line_display)
    print(f"--- [NEXA] Initialization Complete ---")

# --- SYSTEM AUDIO MUTE/UNMUTE FUNCTION ---
def toggle_system_mute(mute_state):
    """
    Mutes (True) or Unmutes (False) the system's output Speaker Sink.
    """
    mute_status = "1" if mute_state else "0"
    
    try:
        subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", mute_status], 
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

# --- ALSA ERROR SUPPRESSION (FIXED) ---
@contextlib.contextmanager
def suppress_alsa_errors():
    """
    Suppresses ALSA/Jack error messages by redirecting stderr.
    """
    try:
        null_fd = os.open(os.devnull, os.O_WRONLY)
        original_stderr_fd = os.dup(sys.stderr.fileno())
        os.dup2(null_fd, sys.stderr.fileno())
        
        yield
        
    finally:
        if 'original_stderr_fd' in locals():
            os.dup2(original_stderr_fd, sys.stderr.fileno())
            os.close(original_stderr_fd)
        if 'null_fd' in locals():
            os.close(null_fd)

# --- Voice Command Listening (SYNTAX FIX) ---
def listen_for_command():
    """
    Listens for a single command, streamlined for speed.
    ALSA/Jack C-level errors are suppressed.
    """
    r = sr.Recognizer()
    audio = None 
    
    try:
        with suppress_alsa_errors():
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=5, phrase_time_limit=8)
        
        print("[NEXA]: Processing audio input...")
        command = r.recognize_google(audio)
        
        print(f"[{USER_NAME}]: {command}")
        return command.lower()

    except sr.WaitTimeoutError:
        print("[NEXA]: Listen timeout. No command was spoken.")
        return None 
    except sr.UnknownValueError:
        print("[NEXA]: I was unable to interpret the audio.")
        return None
    except sr.RequestError as e:
        print(f"[NEXA]: Apologies. The speech recognition service is unavailable: {e}")
        return None
    except Exception as e:
        print(f"[NEXA]: A fault occurred during recognition: {e}")
        return None
        
    finally:
        toggle_system_mute(False)


# --- BASIC QUERY HANDLER ---
def handle_basic_queries(command_text):
    """
    Handles simple, non-action queries like time, date, and identity.
    Returns (True, response_text) if matched, (False, None) otherwise.
    """
    if command_text is None:
        return False, None, None
        
    command_text = command_text.lower()
    
    # --- RE-ORDERED: CONVERSATIONAL FIRST ---
    if "hello" in command_text or "greetings" in command_text:
        return True, random.choice(DIALOGUE["hello"]), None # <-- No state change
    
    if "how are you" in command_text:
        return True, random.choice(DIALOGUE["how_are_you"]), None

    if "thank" in command_text: # Catches "thank you" and "thanks"
        return True, random.choice(DIALOGUE["thank_you"]), None

    if "good morning" in command_text:
        return True, random.choice(DIALOGUE["good_morning"]), None
    
    if "good afternoon" in command_text:
        return True, random.choice(DIALOGUE["good_afternoon"]), None
    
    if "good evening" in command_text:
        return True, random.choice(DIALOGUE["good_evening"]), None

    # --- SYNTAX FIX: Added body to this if statement ---
    if "are you there" in command_text:
        return True, random.choice(DIALOGUE["are_you_there"]), None
    
    if "start typing" in command_text or "dictation mode" in command_text:
        return True, random.choice(DIALOGUE["dictation_on"]), "on" # <-- Set dictation ON
        
    if "stop typing" in command_text or "exit dictation" in command_text:
        return True, random.choice(DIALOGUE["dictation_off"]), "off" # <-- Set dictation OFF

    # --- THEN SPECIFIC QUERIES ---
    if "time" in command_text:
        current_time = datetime.now().strftime("%I:%M %p")
        return True, random.choice(DIALOGUE["time"]).format(time=current_time, user=USER_NAME), None
    
    if "date" in command_text or "today" in command_text:
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return True, random.choice(DIALOGUE["date"]).format(date=current_date, user=USER_NAME), None
        
    if "who are you" in command_text or "your name" in command_text:
        return True, random.choice(DIALOGUE["who_are_you"]).format(name=ASSISTANT_NAME, kernel=platform.release()), None
        
    if "purpose" in command_text:
        return True, random.choice(DIALOGUE["purpose"]).format(user=USER_NAME), None
    
    if "what_can_you_do" in command_text or "capabilities" in command_text:
        return True, random.choice(DIALOGUE["what_can_you_do"]), None

    # --- NEW: Manual Session Restore ---
    if "restore session" in command_text or "open last session" in command_text:
        # This is a special case that requires I/O and logic, so we'll
        # handle the full loop here instead of just returning text.
        
        apps_to_restore = check_for_restore_session()
        
        if apps_to_restore:
            response = random.choice(DIALOGUE["session_restore"]).format(count=len(apps_to_restore))
            print(f"[NEXA]: {response}")
            speak(response)
            
            for app_name in apps_to_restore:
                success, resp_text = open_app(app_name)
                print(f"[NEXA]: {resp_text}")
                time.sleep(0.5) # Stagger launches
            
            # clear_session_note() # <-- DELETED THIS LINE
            return True, "Session restoration complete.", None
            
        else:
            response = random.choice(DIALOGUE["session_restore_fail"]).format(user=USER_NAME)
            return True, response, None

    return False, None, None # <-- Return 3 values

# --- NEW: URL Request Handler ---
def handle_url_request(command_text):
    """
    Parses command for a URL and a specific browser.
    Example: "open google.com in brave"
    """
    # Regex to find a URL-like string
    url_match = re.search(r'([\w-]+\.)+[\w-]+(\.[\w-]+)?', command_text)
    if not url_match:
        return False, None
    
    url = url_match.group(0)
    # Simple check to prepend http:// if it's just a domain
    if not url.startswith("http"):
        url = "https://" + url

    # Regex to find a browser name
    browser_name = BROWSER_PATHS['brave'] # Default
    if "in brave" in command_text:
        browser_name = BROWSER_PATHS['brave']
    elif "in chrome" in command_text:
        browser_name = BROWSER_PATHS['google-chrome']
    elif "in firefox" in command_text:
        browser_name = BROWSER_PATHS['firefox']
        
    success, response_text = open_url(url, browser_name)
    return success, response_text


# --- MUSIC CONTROL HELPER FUNCTION (REVISED FOR PYTHON SOCKET) ---
def send_mpv_command(mpv_command_target):
    """Sends a command to the running MPV instance via direct Unix IPC socket."""
    
    if MUSIC_PLAYER_EXECUTABLE != "mpv":
        return False, random.choice(DIALOGUE["music_control_fail_player"]).format(user=USER_NAME)
        
    if mpv_command_target == "stop":
        # Let's stick to the original logic which was robust
        close_app(MUSIC_PLAYER_EXECUTABLE) # This is 'kill'
        if os.path.exists(MPV_SOCKET_PATH):
            os.remove(MPV_SOCKET_PATH)
            return True, random.choice(DIALOGUE["music_stop"])
        else:
            return False, random.choice(DIALOGUE["music_stop_fail"])

    if not os.path.exists(MPV_SOCKET_PATH):
        return False, random.choice(DIALOGUE["music_control_fail_socket"])

    command_parts = mpv_command_target.split()
    mpv_command = json.dumps({"command": command_parts}) + "\n"
    
    response_text = "Command sent to player."
    if mpv_command_target == "playlist-next":
        response_text = random.choice(DIALOGUE["music_next"])
    elif mpv_command_target == "playlist-prev":
        response_text = random.choice(DIALOGUE["music_prev"])
    elif mpv_command_target == "cycle pause":
        response_text = random.choice(DIALOGUE["music_pause"])
    
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(MPV_SOCKET_PATH)
        s.sendall(mpv_command.encode('utf-8'))
        s.close()
        
        return True, response_text

    except ConnectionRefusedError:
        return False, f"Connection refused, {USER_NAME}. The media socket is locked. I suggest terminating the music playback."
    except FileNotFoundError:
        return False, f"Socket path not found. Please ensure media is playing."
    except Exception as e:
        return False, f"I encountered an error interfacing with the media socket: {e}. Please consider restarting playback."


# --- UPDATED LOCAL PLAYBACK FUNCTION (with IPC socket) ---
def play_local_music(category):
    """
    Starts local music playback for the specified category folder in shuffle mode
    and enables the IPC socket for external control.
    """
    
    category_path = os.path.join(MUSIC_BASE_PATH, category)

    if not os.path.isdir(category_path):
        return False, random.choice(DIALOGUE["music_play_fail_path"]).format(category=category, path=category_path, user=USER_NAME)
    
    music_files = [
        os.path.join(category_path, f) 
        for f in os.listdir(category_path) 
        if f.lower().endswith(('.mp3', '.wav', '.ogg', '.flac', '.m4a'))
    ]
    
    if not music_files:
        return False, random.choice(DIALOGUE["music_play_fail_empty"]).format(category=category)

    try:
        if MUSIC_PLAYER_EXECUTABLE == "mpv":
            # Kill any old instance before starting a new one
            subprocess.run(['pkill', '-9', '-f', 'mpv'], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(MPV_SOCKET_PATH):
                os.remove(MPV_SOCKET_PATH)
                
            command = [
                MUSIC_PLAYER_EXECUTABLE, 
                '--shuffle', 
                '--no-terminal', 
                '--ao=pulse',
                f"--input-ipc-server={MPV_SOCKET_PATH}"
            ] + music_files
        
        elif MUSIC_PLAYER_EXECUTABLE == "vlc":
             return False, "VLC is not currently configured for remote socket control. Please use 'mpv' for full media control features."
        
        else:
             return False, f"The configured media player '{MUSIC_PLAYER_EXECUTABLE}' is not recognized or supported for this action."

        subprocess.Popen(command, 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL,
                         close_fds=True)
        
        return True, random.choice(DIALOGUE["music_play"]).format(count=len(music_files), category=category)
        
    except FileNotFoundError:
        return False, random.choice(DIALOGUE["music_play_fail_player"]).format(player=MUSIC_PLAYER_EXECUTABLE)
    except Exception as e:
        return False, f"An unexpected error occurred while attempting media playback: {e}"

# --- FEATURE HELPER FUNCTION: open_app (REPAIRED) ---
def open_app(exec_name):
    """Opens an application using its executable name."""
    try:
        subprocess.Popen(shlex.split(exec_name), 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL,
                         close_fds=True)
        return True, random.choice(DIALOGUE["app_open"]).format(app=exec_name, user=USER_NAME)
    except FileNotFoundError:
        return False, random.choice(DIALOGUE["app_open_fail"]).format(user=USER_NAME, app=exec_name)
    except Exception as e:
        return False, f"An error occurred while attempting to launch {exec_name}: {e}"

# --- FEATURE HELPER FUNCTION: open_url (RE-ADDED and REPAIRED) ---
def open_url(url, browser_name=BROWSER_PATHS['brave']):
    """
    Opens a URL in the specified browser using subprocess.Popen
    to suppress stdout and stderr.
    """
    try:
        # Ensure URL is complete
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url
        
        # We exclusively use Popen to have full control over output streams
        subprocess.Popen(
            [browser_name, url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True
        )
        return True, random.choice(DIALOGUE["web_open"]).format(url=url, browser=browser_name, user=USER_NAME)
             
    except FileNotFoundError:
        return False, random.choice(DIALOGUE["web_open_fail"]).format(browser=browser_name)
    except Exception as e:
        return False, f"An unexpected error occurred during the web request: {e}"


# --- NEW: Session Note Helper Functions (REPAIRED) ---
def check_for_restore_session():
    """
    Checks if a session note exists and contains app data.
    Returns the list of apps or None.
    """
    if not os.path.exists(SESSION_NOTE_PATH):
        return None
    try:
        with open(SESSION_NOTE_PATH, 'r') as f:
            data = json.load(f)
        if data and isinstance(data, list) and len(data) > 0:
            return data
    except (json.JSONDecodeError, IOError):
        # File is corrupt or empty, clear it
        clear_session_note()
        return None
    return None

def clear_session_note():
    """Writes an empty list to the session note."""
    try:
        with open(SESSION_NOTE_PATH, 'w') as f:
            json.dump([], f)
    except IOError as e:
        print(f"[NEXA_ERROR]: Could not clear session note: {e}")

def save_session_note(app_list):
    """Saves the given list of apps to the session note."""
    try:
        with open(SESSION_NOTE_PATH, 'w') as f:
            json.dump(app_list, f, indent=2)
        print(f"[NEXA]: Session saved with {len(app_list)} applications.")
    except IOError as e:
        print(f"[NEXA_ERROR]: Could not save session note: {e}")

# --- UPDATED FEATURE HELPER FUNCTION: close_app (FINAL TERMINATION FIX) ---
def close_app(exec_name):
    """
    Closes an application by attempting to kill common browser process names
    associated with the executable name (exec_name).
    """
    
    process_name_map = {
        "brave-browser": ["brave", "brave-browser", "brave-nightly", "brave-browser-stable"], 
        "google-chrome": ["chrome", "google-chrome", "google-chrome-stable"],
        "firefox": ["firefox", "firefox-esr", "firefox-bin"],
        "code": ["code", "vscode"],
        "libreoffice": ["soffice", "soffice.bin"],
        "mpv": ["mpv"],
        "vlc": ["vlc"]
    }

    process_names = process_name_map.get(exec_name, [exec_name])
    killed_count = 0
    
    try:
        for name in process_names:
            command = ['pkill', '-9', '-f', name]
            result = subprocess.run(
                command, 
                check=False,
                capture_output=True
            )
            if result.returncode == 0:
                killed_count += 1
        
        if killed_count > 0:
            return True, random.choice(DIALOGUE["app_close"]).format(app=exec_name, user=USER_NAME)
        else:
            return False, random.choice(DIALOGUE["app_close_fail"]).format(app=exec_name, user=USER_NAME)
            
    except FileNotFoundError:
        return False, f"The termination utility ('pkill') was not found. I am unable to force-close applications."
    except Exception as e:
        return False, f"An unexpected error occurred during process termination: {e}"

# --- SYSTEM POWER AND CONTROL FUNCTIONS (FINAL FIX - TERMINAL EXCLUSION) ---

def get_running_process_names():
    """
    Returns a list of common application names to attempt closing on.
    """
    return [
        "brave", "brave-browser", "google-chrome", "firefox", "code", "gedit", 
        "nautilus", "libreoffice", "soffice", "mpv", "vlc",
    ]

def graceful_application_close():
    """Sends a SIGTERM (signal 15, graceful request) to common applications."""
    
    subprocess.run(
        ['pkill', '-15', '-f'] + get_running_process_names(),
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    return True, f"I have sent a graceful shutdown request to all open applications. Allowing {GRACEFUL_CLOSE_DELAY_SECONDS} seconds for you to save any unsaved work, {USER_NAME}."


def perform_system_action(action_type):
    """Handles graceful closure, then executes shutdown/reboot/logout/suspend."""
    
    if action_type == "force_poweroff":
        speak(f"Understood. Initiating an immediate system power-down. Be advised: all unsaved work will be lost.")
        # No session save on force-poweroff
        subprocess.run(["systemctl", "poweroff", "-i"])
        os._exit(0)
        return True, "Force shutdown initiated."

    # --- NEW: Check for running apps *before* closing them ---
    # This is the list of apps we *can* track and restore
    monitored_apps = [
        "brave-browser", "google-chrome", "firefox", "code", 
        "nautilus", "libreoffice", "mpv", "vlc"
    ]
    running_apps_to_save = []
    print("[NEXA]: Checking for running processes to save to session...")
    for app_name in monitored_apps:
        # Use pgrep -f to check if a process with this name is running
        try:
            result = subprocess.run(['pgrep', '-f', app_name], capture_output=True, check=False)
            if result.returncode == 0:
                # Process is running
                running_apps_to_save.append(app_name)
        except FileNotFoundError:
            print("[NEXA_ERROR]: 'pgrep' not found. Cannot save session.")
            running_apps_to_save = [] # Clear list if pgrep fails
            break
    
    # 1. Graceful Close Stage
    graceful_response, graceful_text = graceful_application_close()
    
    # 2. Inform user and wait
    speak(graceful_text)
    print(f"[NEXA]: System halt paused for {GRACEFUL_CLOSE_DELAY_SECONDS} seconds... Please save your files.")
    time.sleep(GRACEFUL_CLOSE_DELAY_SECONDS)
    
    # 3. Aggressive Kill Stage
    speak("Grace period expired. Terminating all remaining user processes.")
    
    app_targets_to_kill = [
        "brave-browser", "google-chrome", "firefox", "code", "nautilus", 
        "libreoffice", "mpv", "vlc"
    ]
    for app_name in app_targets_to_kill:
        close_app(app_name)
    
    if os.path.exists(MPV_SOCKET_PATH):
        os.remove(MPV_SOCKET_PATH)
        
    # 4. Execute the system command
    final_command = None
    action_text = ""
    
    if action_type == "poweroff":
        final_command = ["systemctl", "poweroff"]
        action_text = f"System is powering down. Goodbye, {USER_NAME}."
    elif action_type == "reboot":
        final_command = ["systemctl", "reboot"]
        action_text = "System is rebooting now."
    elif action_type == "suspend":
        final_command = ["systemctl", "suspend"]
        action_text = "Entering suspend mode."
    elif action_type == "logout":
        final_command = ["gnome-session-quit", "--logout", "--force"]
        action_text = "Terminating user session. Logging out."

    if final_command:
        # --- NEW: Save the session just before exiting ---
        if running_apps_to_save:
            save_session_note(running_apps_to_save)
        
        speak(f"Cleanup complete. {action_text}")
        subprocess.run(final_command, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os._exit(0)
        
    return False, "Unknown system action requested."
    
# --- SYSTEM CONTROL FUNCTIONS ---
def set_system_volume(command_text):
    """Sets system master volume using pactl."""
    
    match = re.search(r'(\d+)', command_text)
    if not match:
        return False, random.choice(DIALOGUE["vol_fail_num"]).format(user=USER_NAME)
    
    value = match.group(1)
    
    try:
        if "to" in command_text:
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{value}%"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True, random.choice(DIALOGUE["vol_set"]).format(value=value)
        
        elif "increase" in command_text or "up" in command_text:
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"+{value}%"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True, random.choice(DIALOGUE["vol_up"]).format(value=value)
        
        elif "decrease" in command_text or "down" in command_text:
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"-{value}%"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True, random.choice(DIALOGUE["vol_down"]).format(value=value)
        
        return False, random.choice(DIALOGUE["vol_fail_cmd"]).format(user=USER_NAME)

    except FileNotFoundError:
        return False, random.choice(DIALOGUE["vol_fail_pactl"])
    except Exception as e:
        return False, f"An error occurred while adjusting volume: {e}"

def set_system_brightness(command_text):
    """Sets screen brightness using the xrandr utility (software brightness)."""
    
    match = re.search(r'(\d+)', command_text)
    if not match:
        return False, random.choice(DIALOGUE["bright_fail_num"]).format(user=USER_NAME)
    
    value = int(match.group(1))
    brightness_multiplier = max(0.01, min(1.0, value / 100.0))
    
    try:
        display_output = subprocess.run(['xrandr'], capture_output=True, text=True, check=True).stdout
        primary_match = re.search(r'^(\S+)\s+connected\s+primary', display_output, re.MULTILINE)
        if not primary_match:
            primary_match = re.search(r'^(\S+)\s+connected', display_output, re.MULTILINE)

        if not primary_match:
            return False, random.choice(DIALOGUE["bright_fail_display"])
        
        display_name = primary_match.group(1)
        
        subprocess.run(
            ['xrandr', '--output', display_name, '--brightness', f'{brightness_multiplier:.2f}'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True, random.choice(DIALOGUE["bright_set"]).format(value=value)
        
    except FileNotFoundError:
        return False, random.choice(DIALOGUE["bright_fail_xrandr"])
    except subprocess.CalledProcessError:
        return False, f"The 'xrandr' command failed, {USER_NAME}. I cannot set brightness."
    except Exception as e:
        return False, f"An unexpected error occurred while setting brightness: {e}"

# --- NEW: Continuous Dictation Loop ---
def run_continuous_dictation(keyboard):
    """
    Enters a persistent listening loop to type what the user says.
    Exits when "stop typing" or "exit dictation" is heard.
    Returns False (the new dictation_mode state).
    """
    print(f"[NEXA]: Continuous dictation protocol engaged. Say 'stop typing' to exit.")
    speak("Continuous dictation engaged. I will type everything I hear. Say 'stop typing' to return to command mode.")
    
    r = sr.Recognizer()
    # Adjust sensitivity
    r.pause_threshold = 1.0       # Seconds of non-speaking audio before phrase is complete
    r.non_speaking_duration = 0.5 # Seconds of non-speaking audio to keep on phrase
    r.energy_threshold = 4000     # Default is 300, raise if it picks up too much background noise

    while True:
        try:
            with suppress_alsa_errors():
                with sr.Microphone() as source:
                    # Mute system audio *only* while actively listening
                    toggle_system_mute(True)
                    print("[NEXA_DICTATION]: Listening...")
                    # Listen for a longer phrase
                    audio = r.listen(source, timeout=10, phrase_time_limit=30) 
                    toggle_system_mute(False) # Unmute for processing/typing

            print("[NEXA_DICTATION]: Processing...")
            text = r.recognize_google(audio)
            
            # Check for exit command
            if "stop typing" in text.lower() or "exit dictation" in text.lower():
                print("[NEXA_DICTATION]: Exit phrase detected.")
                response = random.choice(DIALOGUE["dictation_off"])
                print(f"[NEXA]: {response}")
                speak(response)
                break # Exit the while loop
            else:
                # Type the recognized text
                print(f"[NEXA_DICTATION]: Typing... '{text}'")
                keyboard.type(text + " ") # Add a space after typing

        except sr.WaitTimeoutError:
            print("[NEXA_DICTATION]: Timeout, listening again...")
            toggle_system_mute(False) # Ensure unmute on timeout
            continue # Just loop again
        except sr.UnknownValueError:
            print("[NEXA_DICTATION]: Audio not understood.")
            toggle_system_mute(False) # Ensure unmute on error
            continue # Loop again
        except sr.RequestError as e:
            print(f"[NEXA_DICTATION]: Network API Error: {e}")
            speak("My apologies, the speech recognition service appears to be offline.")
            toggle_system_mute(False) # Ensure unmute on error
            time.sleep(1) # Wait a bit before retrying
            continue
        except Exception as e:
            print(f"[NEXA_DICTATION]: A critical error occurred: {e}")
            speak("A critical error has occurred in the dictation module. Exiting.")
            toggle_system_mute(False) # Ensure unmute on error
            break # Exit on unexpected error

    # Ensure system is unmuted on exit
    toggle_system_mute(False)
    return False # Return the new dictation_mode state (which is 'off')


# --- HOTWORD LOOP FUNCTION (MODIFIED) ---
def hotword_loop(pending_restore_list=None):
    """
    Main loop that listens for the hotword 'NEXA' using Porcupine.
    """
    handle = None
    recorder = None
    media_is_playing = False 
    dictation_mode = False # <-- NEW: Dictation state
    keyboard = Controller() # <-- NEW: Keyboard controller
    
    try:
        if not os.path.exists(HOTWORD_MODEL_PATH):
            raise FileNotFoundError(f"Hotword model not found at: {HOTWORD_MODEL_PATH}")
            
        handle = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY, 
            keyword_paths=[HOTWORD_MODEL_PATH] 
        ) 
        
        recorder = PvRecorder(
            device_index=MIC_SOURCE_INDEX, 
            frame_length=handle.frame_length
        )

        # --- NEW: Handle Session Restore on Startup ---
        if pending_restore_list:
            print(f"[NEXA]: Previous session found with {len(pending_restore_list)} applications.")
            prompt = random.choice(DIALOGUE["session_prompt"]).format(count=len(pending_restore_list), user=USER_NAME)
            speak(prompt)
            
            # Manually trigger one listen cycle
            play_system_sound(SOUND_START_LISTEN)
            toggle_system_mute(True)
            print("[NEXA]: Listening for restore confirmation (yes/no)...")
            user_command = listen_for_command()
            # listen_for_command() already unmutes
            play_system_sound(SOUND_DEACTIVATE)

            if user_command and any(word in user_command for word in ["yes", "affirmative", "please", "do it", "restore"]):
                speak("Understood. Restoring previous session.")
                for app_name in pending_restore_list:
                    success, response = open_app(app_name)
                    print(f"[NEXA]: {response}")
                    time.sleep(0.5) # Stagger app launches
            else:
                speak(random.choice(DIALOGUE["session_discard"]).format(user=USER_NAME))
            
            # Clear the session note
            # clear_session_note() # <-- DELETED THIS LINE
        # --- End Session Restore ---

        print(f"\n--- [NEXA] Hotword Detection Activated ---")
        print(f"[NEXA]: Listening for wake-word '{HOTWORD_NAME}'...") 
        recorder.start()

        while True:
            pcm = recorder.read()
            keyword_index = handle.process(pcm)
            
            if keyword_index >= 0:
                print(f"\n[NEXA]: Wake-word detected.")
                
                user_command = None
                
                # 1. Stop Porcupine's recorder *FIRST*
                recorder.stop()

                # 2. Play activation phrase (REPLACED BEEP)
                activation_reply = random.choice(DIALOGUE["activation_phrases"])
                speak(activation_reply)
                
                time.sleep(0.1) 
                
                try:
                    # 4. Play "Start Listening" sound (Still useful feedback)
                    play_system_sound(SOUND_START_LISTEN) 
                    
                    # 5. Mute system output *after* beeps/speech
                    toggle_system_mute(True)
                    
                    print(f"[NEXA]: Listening for command...")
                    
                    # 7. Activate command listening loop
                    user_command = listen_for_command()
                    
                finally:
                    toggle_system_mute(False)
                    
                    if user_command:
                        # --- NEW DICTATION LOGIC ---
                        # We no longer check *if* we are in dictation mode here.
                        # We just process the command, which might *turn on* dictation mode.
                        
                        # --- Normal Command Processing ---
                        media_is_playing, dictation_mode = process_command_logic(user_command, media_is_playing)

                        # --- NEW BLOCK TO HANDLE STARTING DICTATION ---
                        if dictation_mode:
                            # This call will block until dictation is exited
                            # It will return False, setting dictation_mode back to off
                            dictation_mode = run_continuous_dictation(keyboard)
                        
                    # 10. Play "deactivation" beep
                    play_system_sound(SOUND_DEACTIVATE)
                    print(f"[NEXA]: Command cycle complete. [Media: {media_is_playing} | Dictation: {dictation_mode}]. Returning to standby.")
                    
                    # 11. Restart recorder
                    recorder.start()

    except FileNotFoundError as e:
        print(f"\n--- [NEXA_FATAL_ERROR] ---")
        print(f"Configuration Error: {e}")
        print(f"Please ensure the 'HOTWORD_MODEL_PATH' variable is correct.")
    except pvporcupine.PorcupineActivationError as e:
        print(f"\n--- [NEXA_FATAL_ERROR] ---")
        print(f"Picovoice Activation Error: {e}")
        print("This typically indicates an invalid or expired 'PICOVOICE_ACCESS_KEY'.")
    except Exception as e:
        print(f"\n--- [NEXA_FATAL_ERROR] ---")
        print(f"An unexpected hotword loop error occurred: {e}")
        print("Please check microphone permissions, device index, and Picovoice dependencies.")
        
    finally:
        if recorder is not None and recorder.is_recording:
            print("\n[NEXA]: Shutting down... Stopping audio recorder.")
            recorder.stop()
            recorder.delete()
        if handle is not None:
            print("[NEXA]: Releasing Porcupine handle.")
            handle.delete()


# --- COMMAND PROCESSING LOGIC FUNCTION (MODIFIED) ---
def process_command_logic(user_command, current_media_state):
    """
    Handles command parsing outside the hotword loop.
    If no local command is found, it queries the Gemini API.
    Returns: (new_media_state, new_dictation_state)
    """
    
    new_media_state = current_media_state 
    new_dictation_state = False # Default: don't change dictation mode
    command_processed = False
    response_text = ""
    success = False 
    
    # --- 1. Check for NEXA self-termination (program exit) first ---
    if "stop listening" in user_command or "exit" in user_command or "quit" in user_command:
        close_app(MUSIC_PLAYER_EXECUTABLE)
        if os.path.exists(MPV_SOCKET_PATH):
            os.remove(MPV_SOCKET_PATH)
            
        print(f"\n[NEXA]: Executive shutdown confirmed. All systems going offline. Goodbye, {USER_NAME}.")
        speak(f"Executive shutdown confirmed. All systems going offline. Goodbye, {USER_NAME}.")
        os._exit(0)

    # --- 2. NEW: Check for media controls *FIRST* if music is playing ---
    if current_media_state:
        print("[NEXA]: Media playback is active. Prioritizing media control context.")
        media_cmd_processed = False
        
        # Keywords for stopping music
        if any(word in user_command for word in ["stop", "kill", "turn off", "close songs"]):
            success, response_text = send_mpv_command("stop")
            if success:
                new_media_state = False # Update state
            media_cmd_processed = True
            
        # Keywords for next song
        elif "next" in user_command:
            success, response_text = send_mpv_command("playlist-next")
            media_cmd_processed = True
            
        # Keywords for previous song
        elif "previous" in user_command:
            success, response_text = send_mpv_command("playlist-prev")
            media_cmd_processed = True
            
        # Keywords for pause/resume
        elif any(word in user_command for word in ["pause", "resume"]):
            success, response_text = send_mpv_command("cycle pause")
            media_cmd_processed = True
        
        if media_cmd_processed:
            command_processed = True # We handled it.

    # --- 3. BASIC QUERIES (if not processed) ---
    if not command_processed:
        success, response_text, dictation_toggle = handle_basic_queries(user_command)
        if success:
            command_processed = True
            if dictation_toggle == "on":
                new_dictation_state = True
            # No need to check for "off" here, as it's handled by the hotword loop
    
    # --- 4. Volume and Brightness Control (if not processed) ---
    if not command_processed:
        if "volume" in user_command:
            success, response_text = set_system_volume(user_command)
            command_processed = True
        elif "brightness" in user_command:
            success, response_text = set_system_brightness(user_command)
            command_processed = True
            
    # --- 5. NEW: URL Request Parser (if not processed) ---
    if not command_processed:
        # Check for "open" or "launch" + a domain-like string
        if "open" in user_command or "launch" in user_command:
            success, response_text = handle_url_request(user_command)
            if success:
                command_processed = True
    
    # --- 6. DIRECT/ACTION COMMAND CHECK (if not processed) ---
    if not command_processed:
        for friendly_name, data in COMMAND_MAPPING.items():
            
            if user_command == friendly_name:
                target = data['target']
                
                if data['type'] == "music_control":
                    success, response_text = send_mpv_command(target)
                    if success and target == "stop":
                        new_media_state = False # Update state
                    command_processed = True
                    break
                    
                elif data['type'] == "app_music":
                    success, response_text = play_local_music(target)
                    if success:
                        new_media_state = True # Update state
                    command_processed = True
                    break
                    
                elif data['type'] == "system_action": 
                    perform_system_action(target)
                    command_processed = True 
                    break
            
    # --- 7. Generic App/Web Control (if not processed) ---
    if not command_processed:
        for friendly_name, data in COMMAND_MAPPING.items():
            
            target = data['target']
            
            if f"open {friendly_name}" in user_command or f"launch {friendly_name}" in user_command:
                
                if data['type'] == "app":
                    success, response_text = open_app(target)
                    command_processed = True
                    break
                    
                elif data['type'] == "web":
                    browser = data.get('browser', BROWSER_PATHS['brave'])
                    success, response_text = open_url(target, browser)
                    command_processed = True
                    break

            if data['type'] == "app" and (f"close {friendly_name}" in user_command or f"kill {friendly_name}" in user_command):
                success, response_text = close_app(target)
                command_processed = True
                break
    
    # --- 8. FALLBACK: GEMINI API SEARCH (if not processed) ---
    if not command_processed:
        success, response_text = call_gemini_search(user_command)
        command_processed = True # We have now handled the command
    
    # --- 9. Final Output ---
    if not success and not response_text: 
        response_text = random.choice(DIALOGUE["cmd_not_found_local"]).format(user=USER_NAME, command=user_command)
    elif not command_processed and not success: # This case should be rare
        response_text = random.choice(DIALOGUE["cmd_not_found_local"]).format(user=USER_NAME, command=user_command)
    
    print(f"[NEXA]: {response_text}")
    speak(response_text)
    
    # --- 10. Return the new states to the hotword loop ---
    return new_media_state, new_dictation_state
    
# --- Core Execution: MAIN ENTRY POINT IS NOW hotword_loop ---
if __name__ == "__main__":
    
    if os.path.exists(MPV_SOCKET_PATH):
        try:
            os.remove(MPV_SOCKET_PATH)
        except OSError:
            pass 
        
    startup_greeting()
    
    # NEW: Check for session *before* starting the loop
    pending_apps = check_for_restore_session()
    
    # Pass the pending list (or None) to the loop
    hotword_loop(pending_restore_list=pending_apps)

