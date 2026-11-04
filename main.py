import os
import subprocess
from PIL import Image, ImageDraw

os.makedirs("output", exist_ok=True)

story = (
    "एक जंगल में चीकू नाम का खरगोश रहता था। "
    "जंगल में एक शक्तिशाली शेर भी रहता था। "
    "शेर सभी जानवरों को डराता था। "
    "एक दिन चीकू ने अपनी बुद्धि से शेर को सबक सिखाने की योजना बनाई। "
    "चीकू शेर को एक कुएं के पास ले गया। "
    "शेर ने पानी में अपनी परछाई देखी। "
    "वह समझ गया कि ताकत से ज्यादा बुद्धि जरूरी होती है। "
    "सभी जानवर खुशी से रहने लगे।"
)

colors = [
    "#75C9F0",
    "#65B85C",
    "#F6D365",
    "#F39B69",
    "#9B8AE8",
    "#65C9A5"
]

def draw_scene(index, color):
    img = Image.new("RGB", (1080, 1920), color)
    d = ImageDraw.Draw(img)

    # Jungle ground
    d.rectangle((0, 1350, 1080, 1920), fill="#36864B")

    # Sun
    d.ellipse((780, 120, 980, 320), fill="#FFD84D")

    # Trees
    for x in [100, 900]:
        d.rectangle((x, 800, x+80, 1450), fill="#79502B")
        d.ellipse((x-120, 650, x+200, 1050), fill="#267A39")

    # Rabbit
    d.ellipse((180, 1050, 480, 1350), fill="#F5F0E8")
    d.ellipse((230, 880, 300, 1120), fill="#F5F0E8")
    d.ellipse((350, 880, 420, 1120), fill="#F5F0E8")
    d.ellipse((230, 950, 430, 1160), fill="white")
    d.ellipse((280, 1010, 300, 1030), fill="black")
    d.ellipse((360, 1010, 380, 1030), fill="black")
    d.ellipse((315, 1050, 345, 1070), fill="#E88B91")

    # Lion
    d.ellipse((600, 950, 1000, 1370), fill="#B66A28")
    d.ellipse((670, 1020, 930, 1290), fill="#F4C36D")
    d.ellipse((720, 1090, 750, 1120), fill="black")
    d.ellipse((840, 1090, 870, 1120), fill="black")
    d.ellipse((780, 1150, 820, 1190), fill="#713C24")

    # Scene number
    d.text((450, 1700), f"SCENE {index+1}", fill="white")

    img.save(f"output/scene_{index+1:02}.png")

for i, color in enumerate(colors):
    draw_scene(i, color)

# Hindi voice
subprocess.run([
    "espeak-ng", "-v", "hi", "-s", "140",
    "-w", "output/voice.wav", story
], check=True)

# Audio duration
duration = float(subprocess.check_output([
    "ffprobe", "-v", "error",
    "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1",
    "output/voice.wav"
]).decode().strip())

scene_duration = duration / 6

# Video scenes
with open("output/scenes.txt", "w") as f:
    for i in range(1, 7):
        f.write(f"file 'scene_{i:02}.png'\n")
        f.write(f"duration {scene_duration}\n")
    f.write("file 'scene_06.png'\n")

subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", "output/scenes.txt",
    "-i", "output/voice.wav",
    "-vf", "scale=1080:1920,format=yuv420p",
    "-c:v", "libx264",
    "-c:a", "aac",
    "-shortest",
    "-movflags", "+faststart",
    "output/cartoon.mp4"
], check=True)

print("Hindi Cartoon Video Created Successfully!")