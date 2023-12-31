import discord
from discord.ext import commands
from JobFinderBot.scraper import findJobs
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True
client = discord.Client(intents = intents)
load_dotenv()
bot_key = os.getenv('botKey')

@client.event
async def on_ready():
    print(f'logged in as {client.user}(ID:{client.user.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "hello jobfinderbot":
        await message.channel.send('Please specify a valid location. Use one of the following: '
                                   '!findJobs middletown, !findJobs newHaven, !findJobs waterbury, '
                                   '!findJobs stamford, !findJobs hartford. I will find internships that '
                                   'are within 25 miles of your specified location.')
        return

    if message.content.startswith('!findJobs'):
        location = message.content.split(' ')[1].lower() if len(message.content.split(' ')) > 1 else ''

        if location in ['middletown', 'newhaven', 'waterbury', 'stamford', 'hartford']:
            await message.channel.send(f'Searching for jobs within 25 miles of {location.capitalize()}...')
            job_data = await findJobs(location)

            for title, link in job_data:
                response_message = f"**Title:** {title}\n**More Info:** {link}"
                await message.channel.send(response_message)


client.run(bot_key)

