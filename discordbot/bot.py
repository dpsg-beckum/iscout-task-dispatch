import discord
from discord.ext import commands
import json
from pprint import pprint
import json
import redis

r = redis.Redis(host='localhost', port=6379, db=0, protocol=3)

token = json.load(open('secrets.json'))['discord']['bot']['token']


# Create an instance of a bot
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def delete_message_by_id(channel_id, message_id):
    # Convert the channel_id and message_id to integers
    channel_id = int(channel_id)
    message_id = int(message_id)

    # Get the channel object based on the channel_id
    channel = client.get_channel(channel_id)

    if channel:
        try:
            message = await channel.fetch_message(message_id)
            await message.delete()
            return f'Message with ID {message_id} deleted from channel {channel.name}'
        except discord.NotFound:
            return f'Message with ID {message_id} not found'
        except discord.Forbidden:
            return 'Bot does not have permission to delete messages'
    else:
        return 'Channel not found or invalid channel ID'


# Function to send a message to a specific channel by ID
async def send_message_to_channel(channel_id, message):
    # Convert the channel_id to an integer
    channel_id = int(channel_id)

    # Get the channel object based on the channel_id
    channel = client.get_channel(channel_id)

    if channel:
        return(await channel.send(message))
    else:
        return None

# Event: Bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    channel = json.load(open('secrets.json'))['discord']['channels']['taskteam-1']
    msgres =await send_message_to_channel(channel, "Hello World")
    data = json.dumps({"channel" : channel, "msgid":msgres.id})
    print(type(data))
    r.set('taskteam1:currenmsg', data)
    print(type(msgres))
    print(msgres)
    print()
    print(msgres.id)
    print()
    await client.close()
    exit()




async def send(ctx, channel_id, *, message):
    result = await send_message_to_channel(channel_id, message)
    await ctx.send(result)



# Start the bot
print("starting bot")
client.run(token)
print("done")