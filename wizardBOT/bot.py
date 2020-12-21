print("Starting!")
import discord
import os
from discord.ext import commands
import time 
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime
import json
intents = discord.Intents.all()

global foundMessage
foundMessage = False


prefix ='-'
client = commands.Bot(command_prefix=prefix, intents=intents)



#load unload functions
@client.command(hidden=True)
async def load(ctx, extension):
    if ctx.author.id == 226156525419233281:
        client.load_extension(f'cogs.{extension}')
        print(f'Loaded cog: cogs.{extension}')
        await ctx.send(f'``{extension}`` enabled.')
    else:
        await ctx.send('only developers can use this command idiot')

@client.command(hidden=True)
async def reload(ctx, extension):
    if ctx.author.id == 226156525419233281:
        client.unload_extension(f'cogs.{extension}')
        time.sleep(1)
        client.load_extension(f'cogs.{extension}')
        print(f'Reloaded cog: cogs.{extension}')
        await ctx.send(f'``{extension}`` reloaded and enabled.')
    else:
        await ctx.send('only developers can use this command idiot')

@client.command(hidden=True)
async def unload(ctx, extension):
    if ctx.author.id == 226156525419233281:
        client.unload_extension(f'cogs.{extension}')
        print(f'Unloaded cog: cogs.{extension}')
        await ctx.send(f'``{extension}`` disabled.')
    else:
        await ctx.send('only developers can use this command idiot')

for filename in os.listdir("C:/Users/Server/Desktop/wizardBOT/cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded cog: cogs.{filename[:-3]}')

@client.event 
async def on_message_edit(before, after):
    if before.content != after.content:
        if before.author.bot:
            return
        else:
            logchannel = client.get_channel(788643092025966602)
            embed = discord.Embed(
                title = 'Edit Log',
                description = f'```{after.author.display_name} in #{after.channel.name}```',
                colour = discord.Colour.blue()
            )

            embed.add_field(name='Before',value=f"{before.content}",inline=False)
            embed.add_field(name='After',value=f"{after.content}",inline=False)
            embed.add_field(name='Message ID',value=f"{after.id}",inline=False)
            embed.add_field(name='Member ID',value=f"{after.author.id}",inline=False)
            embed.set_author(name=f"{after.author.name}#{after.author.discriminator}")
            embed.timestamp = datetime.now()

            await logchannel.send(embed=embed)

@client.event
async def on_member_join(member):
    guild = client.get_guild(788289267335036948)
    userid = member.id
    filedir = "C:/Users/Server/Desktop/wizardBOT/storage/mutes.json"

    with open(filedir) as json_file:
        mdata = json.load(json_file)
        mutedata = mdata["mutes"]

    for mutedict in mutedata:
        if mutedict.get(str(userid), None):
            userdata = mutedict[str(userid)]
            for role in guild.roles:
                if role.name.lower().startswith("muted"):
                    await member.add_roles(role)
                    return

@client.command(hidden=True)
async def setstatus(ctx, *, status):
    if ctx.author.id == 226156525419233281:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if "sex" in message.content.lower():
        await message.channel.send("wait sex?")

    await client.process_commands(message)

@client.event
async def on_raw_message_delete(payload):
    global foundMessage
    time.sleep(0.1)
    if foundMessage == False:
        message = None
        try:
            message = payload.cached_message
            if message == None:
                message = None
        except Exception as e:
            message = None
        logchannel = client.get_channel(788643092025966602)

        if message:
            if message.author.bot:
                return

        if message:
            embed = discord.Embed(
                title = 'Delete Log',
                description = f'```{message.author.display_name} in #{message.channel.name}```',
                colour = discord.Colour.red()
            )
        else:
            channel = client.get_channel(payload.channel_id)
            embed = discord.Embed(
                title = 'Delete Log',
                description = f'```??? in #{channel.name}```',
                colour = discord.Colour.red()
            )

        if message:
            if message.content:
                embed.add_field(name='Deleted Message Content',value=f"{message.content}",inline=False)
            else:
                embed.add_field(name='Deleted Message Content',value=f"No text was provided.",inline=False)
        else:
            embed.add_field(name='Warning',value=f"Message was not found in the internal message cache, no message content or attachments can be provided.",inline=False)

        embed.add_field(name='Message ID',value=f"{str(payload.message_id)}",inline=False)
        if message:
            embed.add_field(name='Member ID',value=f"{message.author.id}",inline=False)
        else:
            embed.add_field(name='Member ID',value=f"Member ID not found.",inline=False)
        if message:
            embed.set_author(name=f"{message.author.name}#{message.author.discriminator}")
        else:
            embed.set_author(name=f"???")
        embed.timestamp = datetime.now()   

        if message:
            imagelist = []
            for attachment in message.attachments:
                if attachment.height:
                    gotobj = True
                    try:
                        sendable = await attachment.to_file(use_cached=True)
                    except Exception as e:
                        gotobj = False
                        print(e)

                    if gotobj:
                        imagelist.append(sendable)
                        gotobj = False
        
            if message.attachments:
                embed.add_field(name='Image Found',value=f"Any image attachment that was found with this deleted message and has been attached to this log.",inline=False)
                await logchannel.send(files=imagelist,embed=embed)
            else:
                await logchannel.send(embed=embed)  
        else: 
            await logchannel.send(embed=embed)  

                           
@client.command()
async def ping(ctx):
    await ctx.send('pong')

#events

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send(f'Error occured: ``{error}``')

#ready event
@client.event
async def on_ready():
    print(f"Ready \n \n ClientID: {client.user.id} \n ClientUser: {client.user.name} \n Latency: {round(client.latency, 1)}ms \n \n Registered, Connected.")
    
    #watchlistchannel = client.get_channel(788644111481307167)
    #embed = discord.Embed(
        #title = 'Member Watchlist',
        #description = 'Members listed below are subject to increased scrutiny and spectation via moderation.',
        #colour = discord.Colour.dark_gray()
    #)

    #embed.set_footer(text='0/25 total')
    #await watchlistchannel.send(embed=embed)

client.run('LOL U THOUGHT')
print('Loaded bot.py')
