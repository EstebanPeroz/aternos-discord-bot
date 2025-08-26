import os
import discord
from discord import app_commands
from python_aternos import Client
from dotenv import load_dotenv

load_dotenv()
# Enable intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Create command tree
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()  # Sync commands with Discord
    print(f"Logged in as {client.user}")

# Define a slash command
@tree.command(name="minecraft", description="Start minecraft aternos server")
async def minecraft(interaction: discord.Interaction):
    # Initial ephemeral response
    await interaction.response.send_message("Attempting to start the server...", ephemeral=True)
    
    try:
        at = Client()
        at.login(os.getenv("ATERNOS_USERNAME"), os.getenv("ATERNOS_PASSWORD"))

        aternos = at.account
        servs = aternos.list_servers()
        myserv = servs[0]
        myserv.fetch()
        print(myserv.status)

        if myserv.status == "offline":
            myserv.start()
            # Use followup for further messages
            await interaction.followup.send("✅ Server starting", ephemeral=False)
        else:
            await interaction.followup.send("🛑 Server already started", ephemeral=True)
            
    except Exception as e:
        print(e)
        await interaction.followup.send("🛑 An error has occurred.", ephemeral=True)




# Run the bot
client.run(os.getenv("DISCORD_TOKEN"))
