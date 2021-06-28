import os

import discord
import nai
import asyncio
import context
import re
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
NAI_TOKEN = os.getenv("NAI_TOKEN")
CHANNEL_NAME = "omnitea"

DISCORD = discord.Client()
NAI = nai.NAIClient(NAI_TOKEN)
CONTEXT = context.ContextHandler(NAI)

with open("memory.txt", "r") as f:
    MEMORY_TEXT = f.read()

with open("init.txt", "r") as f:
    INITIAL_TEXT = f.read()

CONTEXT.set_memory(MEMORY_TEXT)
CONTEXT.commit_action(INITIAL_TEXT)

def send_message(author, message):
    print(f"==> {author}: {message}")
    CONTEXT.commit_action(f"\n{author} says \"{message}\".\nOmnitea says \"")
    omnitea_message = ""
    while True:
        generation = CONTEXT.generate()
        if '"' in generation:
            message_content = re.findall("([^\"]+)\"(.+)?", generation)[0][0]
            omnitea_message += message_content
            CONTEXT.undo_action()
            CONTEXT.commit_action(f"{message_content}\".")
            break
        else:
            omnitea_message += generation
    print(f"<== Omnitea: {omnitea_message}")
    return omnitea_message


@DISCORD.event
async def on_ready():
    print(f"Logged in as {DISCORD.user.name}")


@DISCORD.event
async def on_message(message):
    if message.author == DISCORD.user:
        return
    if message.channel.name != CHANNEL_NAME:
        return

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, send_message,
                                        message.author.display_name, message.content)
    await message.channel.send(result)


DISCORD.run(DISCORD_TOKEN)
