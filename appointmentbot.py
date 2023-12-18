import discord
import asyncio
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
from dateutil.parser import parse
from datetime import datetime, timedelta

from config import BOT_TOKEN, USER_ID # This is the file that contains your bot token;

# Create a bot instance
bot = commands.Bot(command_prefix='!')

# Scheduler
scheduler = AsyncIOScheduler()

async def call_api():
    # Your API calling code here
    response = requests.get('https://api.appointlet.com/bookables/18433/available_times?service=31057')
    dates = response.json()

    # Get the current date and the date two weeks from now
    now = datetime.now()
    two_weeks_from_now = now + timedelta(weeks=2)

    # Check if the first date is within two weeks
    first_date = parse(dates[0])
    if now <= first_date <= two_weeks_from_now:
        await alert_me()

async def alert_me():
    # Get the User object for your account
    user = bot.get_user(USER_ID)  # Replace 'your_user_id' with your actual Discord user ID

    # Send a DM
    await user.send("Alert: The first date is within two weeks! Visit https://brian-babiak-md.appointlet.com/ for more details.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # Schedule the API call every 10 minutes
    scheduler.add_job(call_api, 'interval', minutes=10)
    scheduler.start()

# Start the bot
bot.run(BOT_TOKEN)
