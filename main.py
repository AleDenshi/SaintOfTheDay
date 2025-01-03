import os
import yaml

from dotenv import load_dotenv
from discord import Intents, Message, File, Object, Interaction, ui, app_commands
from discord.ext import commands, tasks
from responses import get_response
from datetime import datetime

# Open and load config file
config = {}
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
    if config == None:
        print("The config is blank! Writing template...")
        config = {'channels': []}
    file.close()
with open("config.yaml", "w") as file:
    yaml.dump(config, file)
    file.close()	

print(config)


# Loading token from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

# Set up intents and bot
intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)

# Message functionality
async def send_message(channel_id: str, date: str) -> None:
    # Try to send response
    try:
        print("Trying to get the response...")
        response = get_response(date)
        channel = bot.get_channel(channel_id)
        print(response, "<-- the response")
        # Add donate button
        button = ui.Button(label="Donate", url="TODO!!")
        # Create a view to hold the button
        view = ui.View()
        view.add_item(button)
        try: 
            image = File("images/" + date + ".jpg")
            await channel.send(embed=response, file=image, view=view)
        except:
            print("Failed to attach image.")
            await channel.send(embed=response, view=view)

    # Print exception if error occurs
    except Exception as e:
        print(e, "When trying to send message!")

# Function to send messages to all active channels
async def send_saints(date):
    for i in config["channels"]:
        channel = i["channel"]
        utctime = i["utctime"]
        try:
            if utctime == datetime.utcnow().strftime("%H-%M"):
                print("It's", utctime, ", attempting to send the saint of the day for", date, "in channel", channel)
                await send_message(channel, date)
        except Exception as e:
            print(e, "Could not send message in channel", channel + "!")

# DISCORD COMMANDS

# Command to add saints feed to that channel
@bot.tree.command(name="addchannel", description="Adds the Saints of the Day feed to the current channel.")
async def addchannel(interaction: Interaction):
    channel_id = interaction.channel_id
    for entry in config["channels"]:
        if "channel" in entry and entry["channel"] == channel_id:
            await interaction.response.send_message("Sorry, this channel is already being served! Did you mean to run `/removechannel`?", ephemeral=True)
            return
    # Actually add the entry
    try:
        with open("config.yaml", "w") as file:
            print("Adding channel", channel_id)
            # Insert the channel ID, and set default time to 8:00 EST.
            config["channels"].append({"channel" : channel_id, "utctime" : "13-00"})
            yaml.dump(config, file)
            file.close()
        await interaction.response.send_message("Successfully added channel!", ephemeral=True)
    except:
        await interaction.response.send_message("An error occurred trying to add the channel. Please contact the creator of the bot.", ephemeral=True)

# Command to remove saints feed from that channel
@bot.tree.command(name="removechannel", description="Remove the Saints of the Day feed from the current channel.")
async def removechannel(interaction: Interaction):
    channel_id = interaction.channel_id
    for i in range(len(config["channels"])):
        if "channel" in config["channels"][i] and config["channels"][i]["channel"] == channel_id:
            # Actually remove the entry
            try:
                with open("config.yaml", "w") as file:
                    print("Removing channel", channel_id)
                    del config["channels"][i]
                    yaml.dump(config, file)
                    file.close()
                await interaction.response.send_message("Successfully removed channel. Hope to see you again soon!", ephemeral=True)
                return
            except Exception as e:
                print(e)
                await interaction.response.send_message("An error occurred trying to remove the channel. Please contact the creator of the bot.", ephemeral=True)
                return
    await interaction.response.send_message("Sorry, this channel cannot be removed because it's not curretly added! Did you mean to run `/addchannel`?", ephemeral=True)

# Function to parse a time string
def parse_time_string(timestring):
    if ":" not in timestring:
        return None

# TODO TODO Make the time settable
@bot.tree.command(name="settime", description="Set the time (in UTC) when the Saint of the day should be posted in this channel.")
@app_commands.describe(time_to_post = "The time to post the Saint in the following format: HH:MM")
async def settime(interaction: Interaction, time_to_post : str):
    channel_id = interaction.channel_id
    for i in range(len(config["channels"])):
        if "channel" in config["channels"][i] and config["channels"][i]["channel"]:
            existing_time = config["channels"][i]["utctime"]
    print("UNFINISHED")

# Starting up bot
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')
    await bot.tree.sync()
    myloop.start()

# Actually post the Saint of the day
@tasks.loop(seconds=60)
async def myloop():
    time = datetime.now().strftime("%H:%M")
    date = datetime.now().strftime("%m-%d")
    await send_saints(date)

def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()
