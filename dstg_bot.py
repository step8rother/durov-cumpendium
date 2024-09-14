import discord
import aiohttp
import asyncio
import json
from telegram import Bot


with open("/path/to/mapping.json", "r") as m:
    mapping = json.load(m)
with open("/path/to/config.json") as c:
    config = json.load(c)

TELEGRAM_TOKEN = config["TELEGRAM_TOKEN"]
DISCORD_TOKEN = config["DISCORD_TOKEN"]
TELEGRAM_CHAT_ID = config["TELEGRAM_CHAT_ID"]

bot = Bot(token=TELEGRAM_TOKEN)
client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


async def get_voice_channel_members(channel):
    return [member for member in channel.members] if channel is not None else []


@client.event
async def on_voice_state_update(member, before, after):
    voice_channel = after.channel if after.channel is not None else before.channel

    if voice_channel is not None:
        members = await get_voice_channel_members(voice_channel)
        
        active_nicknames = [mapping.get(str(member.id), member.name) for member in members]
        
        with open('/path/to/active_users.txt', 'w') as f:
            f.write('\n'.join(active_nicknames))
        
        if before.channel is None and after.channel is not None:
            telegram_nickname = mapping.get(str(member.id), member.name)
            
            missing_nicknames = [nickname for user_id, nickname in mapping.items() if user_id not in [str(m.id) for m in members]]

            message = (
                f'{telegram_nickname} bounce on channel \n'
                f'Now on channel: {", ".join(active_nicknames)} \n'
                f'Waiting for: {", ".join(missing_nicknames)}'
            )

            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


client.run(DISCORD_TOKEN)
