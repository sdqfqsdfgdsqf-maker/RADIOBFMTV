import subprocess
import time
import audioop
from pymumble_py3 import Mumble

# --- CONFIG DU BOT ---
MUMBLE_HOST = "nocturniaffa.mumble.gg"
MUMBLE_PORT = 10009
MUMBLE_USERNAME = "Radio-MB"
MUMBLE_PASSWORD = ""  # Laisse vide si pas de mdp

# --- PLAYLIST YOUTUBE OU MP3 ---
PLAYLIST = [
    "https://www.youtube.com/watch?v=VT2qF97pQNw&list=PL4QNnZJr8sRN068s0BWzoQJXMPNlUCQQj&index=1",
    "https://www.youtube.com/watch?v=CQ1-ebZItuA&list=RDCQ1-ebZItuA&start_radio=1"
]

# --- FONCTION POUR LANCER L'AUDIO AVEC FFMPEG ---
def play_audio(url):
    process = subprocess.Popen(
        [
            "ffmpeg", "-re", "-i", url,
            "-f", "s16le", "-ar", "48000", "-ac", "1", "pipe:1"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )
    return process

# --- CONNEXION AU SERVEUR MUMBLE ---
m = Mumble(
    MUMBLE_HOST,
    user=MUMBLE_USERNAME,
    port=MUMBLE_PORT,
    password=MUMBLE_PASSWORD
)

m.set_application_string("Radio MB 24/7")
m.start()
m.is_ready()

print("Connecté au Mumble OMGServ !")

# --- LECTURE EN BOUCLE ---
while True:
    for url in PLAYLIST:
        print(f"🎵 Lecture : {url}")
        proc = play_audio(url)

        while True:
            data = proc.stdout.read(1024)
            if not data:
                break

            # --- BAISSER LE VOLUME ICI ---
            # 0.4 = 40% du volume
            data = audioop.mul(data, 2, 0.4)

            # Envoi dans Mumble
            m.sound_output.add_sound(data)

        proc.terminate()
