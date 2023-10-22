import discord
import requests
import random
import openai
from dotenv import load_dotenv
import os

bot = discord.Client(intents=discord.Intents.all())

load_dotenv()
TOKEN = os.getenv('TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if 'john' in message.content.lower():
        
        if(random.randint(1, 100) == 1):
            response = requests.get('https://api.yomomma.info/')
            joke = response.json()['joke']
            await message.channel.send(joke)
        else:
            system_prompt = open("prompt.txt", "r").read()

            channel = message.channel
            recent_messages = []
            async for msg in channel.history(limit=10):
                if msg.author == bot.user:
                    name = "John"
                else:
                    name = msg.author.name if msg.author.name else msg.author.nick
                recent_messages.insert(0, {"role": "user", "content": name + ": " + msg.content})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                #model="gpt-4",
                messages= [{"role": "system", "content": system_prompt}] + recent_messages
            )
            next_message = response["choices"][0]["message"]["content"].replace("John: ", "")
            print(next_message)
            # Check if the message starts with "kick"
            if next_message.lower().startswith("kick "):
                username_to_kick = " ".join(next_message.split()[1:])
                member_to_kick = discord.utils.get(message.guild.members, name=username_to_kick)
                if member_to_kick:
                    try: 
                        await member_to_kick.kick(reason="Kicked by bot command.")
                    except:
                        await message.channel.send(f"Couldn't kick {username_to_kick} as their BMI is beyond fathomable levels.")
                    else:
                        await message.channel.send(f"Kicked {username_to_kick}!")
                else:
                    await message.channel.send(f"Couldn't find a member named '{username_to_kick}'")
            elif next_message.lower().startswith("ban "):
                username_to_ban = " ".join(next_message.split()[1:])
                member_to_ban = discord.utils.get(message.guild.members, name=username_to_ban)
                if member_to_ban:
                    await member_to_ban.ban(reason="Banned by bot command.")
                    await message.channel.send(f"Banned {username_to_ban}!")
                else:
                    await message.channel.send(f"Couldn't find a member named '{username_to_ban}'")
            else:
                await message.channel.send(next_message)

bot.run(TOKEN)
