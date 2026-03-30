import os 
import queue
import uuid
import discord
import asyncio

from google import genai
from google.genai import types
from voicevox import VOICEVOX_ENGINE

#discord.opus.load_opus('/opt/homebrew/lib/libopus.dylib') # for Apple Silicon

###.ENV###
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

###CLIENT###
discord_client = discord.Client(intents=discord.Intents.all())
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

###QUEUE###
q = queue.Queue()

async def play_q(vc_client):
    while not q.empty():
        fname = q.get ()
        print(f"*****NowPlaying:{fname}*****")

        try:
            vc_client.play(discord.FFmpegPCMAudio(fname))
        except Exception as e:
            print(f"*****Playing Error:{e}*****")
        
        while vc_client.is_playing():
            await asyncio.sleep(0.5)
        
        try:
            os.remove(fname)
            print(f"*****Audio Source Removed:{fname}*****")
        except Exception as e:
            print(f"*****Removing Error:{e}*****")

###LOG_IN###
@discord_client.event
async def on_ready():
    print('Logged in.')

###MAIN###
@discord_client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if "http://" in message.content or "https://" in message.content:
        return

    received_message = message.clean_content
    if len(received_message) > 100:
        received_message = received_message[:100]
        print("*****Cutoff for Fast Processing*****")

    vc_client = message.guild.voice_client
        
    if received_message:
        if discord_client.user in message.mentions:
            content = message.content.replace(message.guild.me.mention, "").strip()

            if message.guild.voice_client is None:
                await message.channel.send("Not connected")
                return
            
            response = gemini_client.models.generate_content(
                model='gemini-3.1-flash-lite-preview',
                contents=(received_message),
                config=types.GenerateContentConfig(
                     system_instruction="あなたの名前はずんだもんです。日本語で会話してください。一人称は僕にしてください。100文字以内で回答してください。また、語尾を文脈に応じて次のように変更してください。「んです」に置き換え可能な場合→のだ/「である」に置き換え可能な場合→なのだ"
                )
            )
            print(response.text)
            await message.channel.send(response.text)

            fname_gemini = (f"voice_{uuid.uuid4()}.mp3")
            VOICEVOX_ENGINE(text = response.text, speaker = 3, audio_file = fname_gemini)
            
            q.put(fname_gemini)
            print(f"Queued:{fname_gemini}")
            if not vc_client.is_playing():
                await play_q(vc_client)
        
        elif received_message =="!join":
            if message.author.voice is None:
                await message.channel.send('Please connect to the voice channel.')
                return
            
            await message.author.voice.channel.connect()
            await message.channel.send('VOICE CONNECTED.')
        
        elif received_message =="!leave":
            if message.guild.voice_client is None:
                await message.channel.send('Not connected.')
                return
        
            await message.guild.voice_client.disconnect()
            await message.channel.send('Disconnected.')   
            
        else:
            if message.author.voice is None or message.guild.voice_client is None:
                return
            
            fname_chat = (f"voice_{uuid.uuid4()}.mp3")
            VOICEVOX_ENGINE(text = received_message, speaker = 3, audio_file = fname_chat)
            
            q.put(fname_chat)
            print(f"*****Qed:{fname_chat}*****")
            if not vc_client.is_playing():
                await play_q(vc_client)

###AUTO_DISCONNECT###
@discord_client.event
async def on_voice_state_update(member, before, after):

    if member.bot:
        return
    
    vc_client2 = member.guild.voice_client
    
    if before.channel is not None and before.channel != after.channel:


        if vc_client2 and vc_client2.channel == before.channel:
            if len(vc_client2.channel.members) == 1:
                await vc_client2.disconnect()
                print(f"*****Disconnected.*****")

###RUN###
discord_client.run(DISCORD_TOKEN)