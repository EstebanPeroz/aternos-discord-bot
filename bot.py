import os
import discord
import asyncio
from discord import app_commands
from python_aternos import Client
from dotenv import load_dotenv

load_dotenv()
# Enable intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
ATERNOS_USERNAME = os.getenv("ATERNOS_USERNAME")
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")

async def update_bot_status(status: str):
    """Update the bot's Discord status."""
    print(status)
    if "online" in status:
        statusDiscord = discord.Status.online
    elif "offline" in status:
        statusDiscord = discord.Status.dnd
    else:
        print("Probably starting...")
        statusDiscord = discord.Status.idle
    await client.change_presence(activity=discord.Game(name=status), status=statusDiscord)


async def status_loop():
    await client.wait_until_ready()  # Wait for bot to connect
    at = Client()
    at.login(ATERNOS_USERNAME, ATERNOS_PASSWORD)
    aternos = at.account
    servs = aternos.list_servers()
    myserv = servs[0]

    while not client.is_closed():
        try:
            myserv.fetch()  # Get latest server status
            server_status = myserv.status
            await update_bot_status(f"Aternos server: {server_status}")
        except Exception as e:
            print(f"Error fetching server status: {e}")
            await update_bot_status("Error fetching server status")
        
        await asyncio.sleep(60)

@client.event
async def on_ready():
    await tree.sync()  # Sync commands with Discord
    print(f"Logged in as {client.user}")
    client.loop.create_task(status_loop())

# Define a slash command
@tree.command(name="start", description="Start minecraft server")
async def start(interaction: discord.Interaction):
    # Initial ephemeral response
    await interaction.response.send_message("Attempting to start the server...", ephemeral=True)
    
    try:
        at = Client()
        at.login(ATERNOS_USERNAME, ATERNOS_PASSWORD)

        aternos = at.account
        servs = aternos.list_servers()
        myserv = servs[0]
        myserv.fetch()
        print(myserv.status)

        await update_bot_status(f"Status: {myserv.status}")
        
        if myserv.status == "offline":
            myserv.start()
            # Use followup for further messages
            await interaction.edit_original_response(content="✅ Server starting")
        else:
            await interaction.edit_original_response(content=f"🛑 Server not offline.\nCurrent status: ***{myserv.status}***")
            
    except Exception as e:
        print(e)
        await interaction.edit_original_response(content=f"🛑 An error has occurred.")


# Run the bot
client.run(os.getenv("DISCORD_TOKEN"))
