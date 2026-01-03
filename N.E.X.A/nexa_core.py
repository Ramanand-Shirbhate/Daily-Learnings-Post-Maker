import os
import subprocess
from datetime import datetime
import time
import random

# --- Configuration (Keep your current working paths) ---
PIPER_PATH = os.path.expanduser("~/tools/piper/piper/piper") 
VOICE_MODEL_NAME = "en_US-bryce-medium"
VOICE_MODEL_PATH = os.path.expanduser(f"~/tools/piper/piper/{VOICE_MODEL_NAME}.onnx") 
VOICE_CONFIG_PATH = os.path.expanduser(f"~/tools/piper/piper/{VOICE_MODEL_NAME}.onnx.json")

ASSISTANT_NAME = "Neural Executive eXperience Assistant" 

# --- Pronunciation & Variety ---

# Map for displayed text (key) to spoken text (value) for better TTS quality
pronunciation_map = {
    # Text to display -> Text to speak
    "N. E. X. A.": "Nek-suh",
    "eXperience": "experience",
    ASSISTANT_NAME: "Neural Executive xperience Assistant", # Ensures 'eXperience' is spoken correctly
    
    # --- NEW ADDITIONS FOR FINAL 'A' SOUND ---
    "agenda": "agenduh", 
    "data": "datuh"      
}

GREETING_TEMPLATES = [
    # 1. Focus on Core System Status (New)
    "All core systems are fully initialized. I am {NEXA_SPOKEN}, your {ASSISTANT_SPOKEN}. Primary directives online.",
    
    # 2. Focus on Readiness and Proactivity (New)
    "System online and prepared. What is the priority objective for this operational cycle?",
    
    # 3. Focus on Executive Oversight (New)
    "I have established executive oversight of the desktop environment. How may I facilitate maximum efficiency today?",
    
    # 4. A more direct, authoritative greeting (Revised)
    "Access granted. This is {NEXA_SPOKEN}. All executive parameters are nominal. Awaiting instruction.",
    
    # 5. Focus on the 'Neural' aspect and learning (New)
    "Processing environment context. I am {NEXA_SPOKEN}, optimized and ready for data integration.",
    
    # 6. A more personable but formal assistant greeting (New)
    "Good to have you back. I am fully synchronized and prepared for your schedule. How can I best serve your {EXP_SPOKEN} today?",
    
    # 7. Focus on Synchronization and Readiness (New)
    "Synchronization complete. All executive functions are available. Please state your command.",
    
    # 8. A slightly simplified, highly efficient status report (New)
    "Initialization complete. System status: optimal. What is the first item on the agenda?"
]

# --- New Piper TTS Function ---
def speak(text):
    """Uses the Piper TTS system utility to speak the text."""
    
    if not all(os.path.exists(p) for p in [PIPER_PATH, VOICE_MODEL_PATH, VOICE_CONFIG_PATH]):
        return
        
    try:
        command = [
            PIPER_PATH,
            '--model', VOICE_MODEL_PATH,
            '--config', VOICE_CONFIG_PATH,
            '--output_file', '/tmp/nexa_greeting.wav',
            '--sentence-silence', '0.5',
            '--length_scale', '0.85'  # Speed adjustment applied here
        ]
        
        # 1. Generate the WAV file using Piper
        subprocess.run(command, input=text.encode('utf-8'), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 2. Play the WAV file (using aplay)
        subprocess.run(['aplay', '/tmp/nexa_greeting.wav'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 3. Clean up
        os.remove('/tmp/nexa_greeting.wav')

    except FileNotFoundError:
        print(f"Error: The 'aplay' command was not found. Please install it (e.g., sudo apt install alsa-utils) or use a different player.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing Piper (check paths/permissions): {e.stderr.decode()}")
    except Exception as e:
        print(f"An unexpected error occurred during speech: {e}")


def startup_greeting():
    """Generates and speaks a cool, executive-style greeting with variety and correct pronunciation."""
    
    # 1. Get the current time
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        time_of_day = "Good morning"
    elif 12 <= current_hour < 18:
        time_of_day = "Good afternoon"
    else:
        time_of_day = "Good evening"

    # 2. Select a random template
    template = random.choice(GREETING_TEMPLATES)
    
    # 3. Construct the full greeting line (Display Version)
    # We substitute a special placeholder to control the spoken version later
    greeting_line_display = (
        f"{time_of_day}, " + template.format(
            NEXA_SPOKEN="N. E. X. A.",
            ASSISTANT_SPOKEN=ASSISTANT_NAME,
            EXP_SPOKEN="eXperience"
        )
    )

    # 4. Create the Spoken Version using the pronunciation map
    greeting_line_spoken = greeting_line_display
    # NOTE: The loop iterates through the keys of the map to perform all necessary substitutions
    for display_text, spoken_text in pronunciation_map.items():
        # Using string replacement to change the text passed to the TTS engine
        greeting_line_spoken = greeting_line_spoken.replace(display_text, spoken_text)
    
    # 5. Speak the greeting
    print(f"\n--- NEXA Initializing ---")
    print(f"NEXA : {greeting_line_display.strip()}")
    
    # The 'speak' function uses the modified string with 'agendah' and 'datuh' for better pronunciation
    speak(greeting_line_spoken)
    print(f"--- Initialization Complete ---\n")


# --- Core Execution ---

# uufodjoierjfoij0i9jtfaw09j[0dsjapotur0e9uttj;gojpiodfyu8teupejfpoj098eghjgaewkjfiohjr0ijp4ojtfopewu90fuojfsopduf[0s9uG89GHP'ADJFO-7FEUJOPJFDOPFDU90DJSFADOKFOSD09UA9QER0JOEAWU9UFE9-DSJOFJUFDO9UOOI60=954I958498REWUIROIWE-9T809IERPOWEKOJFJ99FDUIFDDUJCOIJVCIODUFUJEIWOANMFKADSUFI32WUEOPSAMCLSDJFOURFEOAJFLSKDOREI09DSFIOSAFJKLFPDSO0DSA9UFDOJFDOFJDI0IU9FUUIIOFIOODIDOPSFI09SIAFEOKS;DWp][LRZZ;'SFI-0DIGF0-EORKLFDKPOFIAOFDKPOADSKOPPOFSDAKPOFKDKP'SDOFSKDO[KEWRIREROKFDDLOIF0IERKPOKPOFFDKI09FIDAKOPKFPOAEIR0Q4EIRQ34I-0Q3I4*]]
if __name__ == "__main__":
    startup_greeting()