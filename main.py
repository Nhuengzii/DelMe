import nextcord
from nextcord.ext import commands
import os
from deepface import DeepFace
import requests
import pandas as pd
from dotenv import load_dotenv

# Setup intents
intents = nextcord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(intents=intents)


def is_image(filename: str):
    return filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg")

def save_image(url: str, filename: str):
    with open(filename, "wb") as f:
        response = requests.get(url, stream=True)
        if not response.ok:
            print(response)
            return
        for block in response.iter_content(1024):
            if not block:
                break
            f.write(block)

def contains_me(url: str):
    save_image(url, "image.jpg")
    res: list[pd.DataFrame] =  DeepFace.find(img_path="./image.jpg", db_path="./me", enforce_detection=False, model_name="Facenet512")
    print(res)
    for item in res:
        if len(item.to_numpy()) > 1:
            return True
    return False

@bot.event
async def on_ready():
    print("Ready!")

@bot.event
async def on_message(message: nextcord.Message):
    if message.author.bot:
        return
    for attachment in message.attachments:
        if not is_image(attachment.filename):
            continue
        if contains_me(url=attachment.url):
            print("Found me!")
            await message.channel.send("ส่งมาทำไมครับ")
            return
        
        
load_dotenv()
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("Please set TOKEN in .env file")
    exit(1)
bot.run(TOKEN)
