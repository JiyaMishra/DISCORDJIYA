import discord
import asyncio
import datetime
import pytz
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

BOT_SECRET = os.getenv("DISCORD_TOKEN")
AI_SECRET = os.getenv("GEMINI_API_KEY")

if not BOT_SECRET or not AI_SECRET:
    raise ValueError("Missing Discord token or Gemini API key.")

genai.configure(api_key=AI_SECRET)
ai_model = genai.GenerativeModel('gemini-pro')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Client(intents=intents)

reminders = {}
polls = {}
music_queues = {}

def convert_time(time_text):
    formats = [
        '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M', '%m/%d/%Y %H:%M',
        '%H:%M %d/%m/%Y', '%H:%M %m/%d/%Y',
        '%Y-%m-%d %I:%M%p', '%d/%m/%Y %I:%M%p', '%m/%d/%Y %I:%M%p',
        '%I:%M%p %d/%m/%Y', '%I:%M%p %m/%d/%Y',
    ]
    for format_string in formats:
        try:
            time_obj = datetime.datetime.strptime(time_text, format_string)
            return pytz.utc.localize(time_obj)
        except ValueError:
            pass
    return None

async def send_a_reminder(user_id, reminder):
    user = bot.get_user(user_id)
    if user:
        try:
            await user.send(f"Reminder: {reminder['message']}")
        except discord.Forbidden:
            print(f"Can't send a message to {user_id}.")
        if user_id in reminders and reminder in reminders[user_id]:
            reminders[user_id].remove(reminder)
            if not reminders[user_id]:
                del reminders[user_id]

async def check_for_reminders():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.datetime.now(pytz.utc)
        for user_id, user_reminders in list(reminders.items()):
            for reminder in list(user_reminders):
                if reminder['time'] <= now:
                    await send_a_reminder(user_id, reminder)
        await asyncio.sleep(60)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(check_for_reminders())
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"Welcome, {member.mention}!")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    content = message.content.lower()

    if content.startswith("!remind"):
        parts = message.content.split(" ", 2)
        if len(parts) == 3:
            time_text, reminder_message = parts[1], parts[2]
            reminder_time = convert_time(time_text)
            if reminder_time:
                user_id = message.author.id
                new_reminder = {"time": reminder_time, "message": reminder_message}
                if user_id not in reminders:
                    reminders[user_id] = []
                reminders[user_id].append(new_reminder)
                await message.channel.send(f"Reminder set for {reminder_time.strftime('%Y-%m-%d %H:%M %Z')}: {reminder_message}")
            else:
                await message.channel.send("Invalid time format. Please use a valid date-time format.")

    elif content.startswith("!poll"):
        parts = message.content.split(" ", 2)
        if len(parts) > 2:
            question, options_str = parts[1], parts[2]
            options = options_str.split(",")
            if len(options) >= 2:
                embed = discord.Embed(title=question, description="\n".join([f"{i+1}. {option.strip()}" for i, option in enumerate(options)]))
                poll_message = await message.channel.send(embed=embed)
                for i in range(len(options)):
                    await poll_message.add_reaction(f"{i+1}️⃣")
                polls[poll_message.id] = {"question": question, "options": [o.strip() for o in options], "votes": {}}
    elif content.startswith("!summarize"):
        text = message.content[len("!summarize"):].strip()
        try:
            response = ai_model.generate_content(f"Summarize:\n{text}")
            await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send(f"Error: {e}")
    elif content.startswith("!play"):
        song_name = message.content[len("!play"):].strip()
        server_id = message.guild.id
        if server_id not in music_queues:
            music_queues[server_id] = []
        music_queues[server_id].append(song_name)
        await message.channel.send(f"Added '{song_name}' to the queue.")
    elif content.startswith("!queue"):
        server_id = message.guild.id
        if server_id in music_queues and music_queues[server_id]:
            queue_list = "\n".join([f"{i+1}. {song}" for i, song in enumerate(music_queues[server_id])])
            await message.channel.send(f"Music Queue:\n{queue_list}")
        else:
            await message.channel.send("The queue is empty.")

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    if reaction.message.id in polls:
        poll = polls[reaction.message.id]
        if str(reaction.emoji) in [f"{i+1}️⃣" for i in range(len(poll["options"]))]:
            option_index = int(reaction.emoji[0]) - 1
            if reaction.message.id not in poll["votes"]:
                poll["votes"][reaction.message.id] = {}
            poll["votes"][reaction.message.id][user.id] = option_index
bot.run(BOT_SECRET)
