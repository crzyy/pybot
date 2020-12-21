import discord
import os
from discord.ext import commands, tasks
from discord import Intents
import time 
from file_read_backwards import FileReadBackwards
import thread
import json
from datetime import datetime
from datetime import timedelta
import random

global guildid 
guildid = 788289267335036948



class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mutetick.start()
        self.bantick.start()
        
    #@commands.command()
    #@commands.has_permissions(manage_roles=True)
    #async def removeroles(self,ctx, member : discord.Member):
        #for role in member.roles:
           # if "everyone" in role.name:
                #print('lol')
           # else:
              #  await member.remove_roles(role)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, memberindentif, rolename):
        if ctx.author.bot:
            return

        member = await returnmember(self.client,ctx, memberindentif)
        logchannel = self.client.get_channel(788643092025966602)

        belowrole = isbelowrole(ctx, member.id, ctx.author.id)

        if belowrole and ctx.author.id != 226156525419233281:
            await ctx.send(f"<@{ctx.author.id}>, You cannot execute commands on people equal to or above you.")
            return     
        
        for role in member.roles:
            if role.name.lower().startswith(rolename.lower()):
                await member.remove_roles(role)
                await ctx.send(f"<@{ctx.author.id}>, Successfully **removed** role ``{role.name}`` from {member.display_name}")

                embed = discord.Embed(
                    title = 'Role Log',
                    description = f'{ctx.author.display_name} has **removed** role ``{role.name}`` from {member.display_name}',
                    colour = discord.Colour.dark_orange()
                )
                
                embed.timestamp = datetime.now()
                await logchannel.send(embed=embed)
                return

        for role in ctx.guild.roles:
            if role.name.lower().startswith(rolename.lower()):
                await member.add_roles(role)
                await ctx.send(f"<@{ctx.author.id}>, Successfully **gave** role ``{role.name}`` to {member.display_name}")

                embed = discord.Embed(
                    title = 'Role Log',
                    description = f'{ctx.author.display_name} has **given** role ``{role.name}`` to {member.display_name}',
                    colour = discord.Colour.dark_orange()
                )
                embed.timestamp = datetime.now()

                await logchannel.send(embed=embed)
                return
        


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearchannel(self,ctx):
        await ctx.send(f'Clearing all messages in the entirety of ``{ctx.channel.name}``.')
        time.sleep(3)
        await ctx.channel.purge(limit=100000)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx, *, amount):
        amount = int(amount)
        amount = amount + 2
        await ctx.send(f'Clearing ``{amount}`` messages in ``{ctx.channel.name}``.')
        time.sleep(1)
        await ctx.channel.purge(limit=amount)
        

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, member : discord.Member, *, reason="No reason provided."):
        logchannel = self.client.get_channel(788321126160924690)
        if member.id == ctx.author.id:
            await ctx.send(f"<@{ctx.author.id}>, You cannot execute commands on yourself.")
            return

        belowrole = isbelowrole(ctx, member.id, ctx.author.id)

        if belowrole and ctx.author.id != 226156525419233281:
            await ctx.send(f"<@{ctx.author.id}>, You cannot execute commands on people equal to or above you.")
            return       

        global isBeingKicked
        isBeingKicked = True
        membername = f'{member.name}#{member.discriminator}'
        dm = await member.create_dm()

        embed = discord.Embed(
            title = f'You have been kicked from {ctx.guild.name}',
            description = 'You may rejoin the discord at any time.',
            colour = discord.Colour.dark_gray()
        )

        embed.timestamp = datetime.now()
        embed.add_field(name="Moderator Note", value=f"{reason}", inline=False)
        embed.add_field(name="Links", value=f"[Appeal Form](https://docs.google.com/forms/d/e/1FAIpQLSfZwN69hB8aPs8QtvzqO1LSRvAxxkws13TS6ZeqEf90pXjUMA/viewform?usp=sf_link)\n[Community Guidelines](https://discord.com/guidelines)", inline=False)
        try:
            await dm.send(embed=embed)
        except Exception:
            print("couldn't dm")


        await member.kick(reason=reason)
        await ctx.send(f'<@{ctx.author.id}>, You have kicked ``{membername}`` with reason ``{reason}`` ')
        


        embedVar = discord.Embed(title="Member Kicked!", description=f"```{membername} has been kicked from the discord by {ctx.author.display_name}```", color=0xffcd42)
        embedVar.add_field(name="Note", value=f"{reason}", inline=False)
        embedVar.timestamp = datetime.now()
        
        await logchannel.send(embed=embedVar)
        isBeingKicked = False

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, username, *, reason="No reason provided."):
        logchannel = self.client.get_channel(788321126160924690)
        bans = await ctx.guild.bans()       

        for ban_entry in bans:
            if username.isdigit():
                if ban_entry.user.id == int(username):
                    username = ban_entry.user.name


            if ban_entry.user.name.lower().startswith(username.lower()):

                membername = f"{ban_entry.user.name}#{ban_entry.user.discriminator}" 
                await ctx.guild.unban(ban_entry.user)
                await ctx.send(f'<@{ctx.author.id}>, You have unbanned ``{membername}`` with reason ``{reason}`` ')

                filedir = "C:/Users/Server/Desktop/wizardBOT/storage/bans.json"
                with open(filedir) as json_file:
                    userid = ban_entry.user.id
                    data = json.load(json_file)
                    bandata = data["bans"]

                    for element in bandata:
                        if f'{str(userid)}' in element:
                            del element[f'{str(userid)}']

                        with open(filedir, 'w') as data_file:
                            json.dump(bandata, data_file)
                            didTheThing = True

                write_json(data,filedir)


                embedVar = discord.Embed(title="Member Unbanned!", description=f"```{membername} has been unbanned from the discord by {ctx.author.display_name}```", color=0x4bff42)
                embedVar.add_field(name="Note", value=f"{reason}", inline=False)
                embedVar.timestamp = datetime.now()    

                await logchannel.send(embed=embedVar)
                return

        await ctx.send(f'<@{ctx.author.id}>, User ``{username}`` was not found in any ban entries. Try to be more specific.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, membern, *, dateandreason=None):
        member = await returnmember(self.client,ctx, membern)
        reason,time = await returndateandreason(ctx, dateandreason)

        if dateandreason == None:
            reason = "No reason provided."
            time = "01/01/2050 12:00 AM"

        if time == None:
            return
        isInServer = True

        if member == None:
            if membern.isdigit():
                try:
                    member = await self.client.fetch_user(int(membern))
                    isInServer = False
                except Exception:
                    await ctx.send(f"<@{ctx.author.id}>, Couldn't find user ``{membern}``")
                    return
            else:
                await ctx.send(f"<@{ctx.author.id}>, Couldn't find user ``{membern}``")
                return


        logchannel = self.client.get_channel(788321126160924690)

        belowrole = isbelowrole(ctx, member.id, ctx.author.id)


        if member.id == ctx.author.id:
            await ctx.send(f"<@{ctx.author.id}>, You cannot execute commands on yourself.")
            return

        if belowrole and ctx.author.id != 226156525419233281:
            await ctx.send(f"<@{ctx.author.id}>, You cannot execute commands on people equal to or above you.")
            return       

        global blockEvent
        blockEvent = True
        membername = f'{member.name}#{member.discriminator}'
        if isInServer:
            dm = await member.create_dm()

        embed = discord.Embed(
            title = f'You have been banned from {ctx.guild.name}',
            description = '',
            colour = discord.Colour.dark_gray()
        )

        embed.add_field(name="Moderator Note", value=f"{reason}", inline=False)
        embed.add_field(name="Expiration", value=f"{time} CT (UTC-6:00)", inline=False)
        embed.add_field(name="Links", value=f"[Appeal Form](https://docs.google.com/forms/d/e/1FAIpQLSfZwN69hB8aPs8QtvzqO1LSRvAxxkws13TS6ZeqEf90pXjUMA/viewform?usp=sf_link)\n[Community Guidelines](https://discord.com/guidelines)", inline=False)


        filedir = "C:/Users/Server/Desktop/wizardBOT/storage/bans.json"
        with open(filedir) as json_file:
            userid = member.id
            data = json.load(json_file)
            bandata = data["bans"]

            y = {
                f"{userid}": {
                    "expires": str(time)
                }
            }

            for element in bandata:
                if f'{str(userid)}' in element:
                    del element[f'{str(userid)}']

                with open(filedir, 'w') as data_file:
                    json.dump(bandata, data_file)

            bandata.append(y)
        write_json(data,filedir)

        if isInServer:
            try:
                await dm.send(embed=embed)
            except Exception as e:
                print("couldnt dm")
            await member.ban(reason=reason)
        else:
            await ctx.guild.ban(member)

        await ctx.send(f'<@{ctx.author.id}>, You have banned ``{membername}`` until ``{time} CT`` with reason ``{reason}`` ')

        embedVar = discord.Embed(title="Member Banned!", description=f"```{membername} has been banned from the discord until {time} CT by {ctx.author.display_name}```", color=0xe6493e)
        embedVar.add_field(name="Note", value=f"{reason}", inline=False)
        
        await logchannel.send(embed=embedVar)
        await write_modlog(self.client,ctx,member.id,time,"Ban",reason,ctx.author.id)
        blockEvent = False
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def addwatchlist(self, ctx, membername, *, reason):
        watchlistchannel = self.client.get_channel(788644111481307167)
        watchlist = await watchlistchannel.fetch_message(788651389516775454)
        watchlistembed = watchlist.embeds[0]
        numoffields = 0

        for fields in watchlistembed.fields:

            if fields != None:
                numoffields=numoffields+1
            else:
                numoffields = 0

        if numoffields >= 25:
            await ctx.send(f'<@{ctx.author.id}>, The watchlist has reached the maximum limit of members.')
            return

        await watchlist.edit(
            embed=watchlist.embeds[0].add_field(name=f'{membername} - Added by {ctx.author.display_name}', value=f'Note: {reason}', inline=False)
            )

        if ctx.message.author.name.startswith(membername):
            await ctx.send(f'<@{ctx.author.id}>, You cannot add yourself to the watchlist.')
            return

        numoffields = 0
        for fields in watchlistembed.fields:

            if fields != None:
                numoffields=numoffields+1
            else:
                numoffields = 0

        await watchlist.edit(
            embed=watchlist.embeds[0].set_footer(text=f'{numoffields}/25 total')
            )

        await ctx.send(f'<@{ctx.author.id}>, Added ``{membername}`` to the watchlist.')
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def removewatchlist(self, ctx, membername):
        watchlistchannel = self.client.get_channel(788644111481307167)
        watchlist = await watchlistchannel.fetch_message(788651389516775454)
        watchlistembed = watchlist.embeds[0]
        numoffields = 0
        interated = 0

        for field in watchlistembed.fields:
            interated = interated+1
            if field == None:
                await ctx.send(f'<@{ctx.author.id}>, There are no fields in the watchlist.')
                return
            else:
                if membername in field.name:
                    watchlistembed.remove_field(interated-1)
                    await ctx.send(f'<@{ctx.author.id}>, Removed ``{membername}`` from the watchlist.')
                    break

        for fields in watchlistembed.fields:

            if fields != None:
                numoffields=numoffields+1
            else:
                numoffields = 0
                
        await watchlist.edit(
            embed=watchlist.embeds[0].set_footer(text=f'{numoffields}/25 total')
            )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearwatchlist(self, ctx):
        watchlistchannel = self.client.get_channel(788644111481307167)
        watchlist = await watchlistchannel.fetch_message(788651389516775454)

        embed = discord.Embed(
            title = 'Player Watchlist',
            description = 'Players noted on this list should be watched carefully by Moderators.',
            colour = discord.Colour.dark_gray()
        )

        embed.set_footer(text='0/25 total')

        await watchlist.edit(embed=embed)
        await ctx.send(f'<@{ctx.author.id}>, Cleared the watchlist.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, memberidentification, *, dateandreason=None):
        reason,time = await returndateandreason(ctx, dateandreason)

        if dateandreason == None:
            reason = "No reason provided."
            time = "01/01/2050 12:00 AM"

        logchannel = self.client.get_channel(788321126160924690)
        member = await returnmember(self.client,ctx, memberidentification)
  
        if member.id == ctx.author.id:
            await ctx.send(f'<@{ctx.author.id}>, You cannot mute yourself!')
            return

        memberid = member.id
        belowrole = isbelowrole(ctx, member.id, ctx.author.id)

        if belowrole and ctx.author.id != 226156525419233281:
            await ctx.send(f"<@{ctx.author.id}>, You cannot execute commands on people equal to or above you.")
            return       

        for role in member.roles:
            if role.name.lower().startswith("muted"):
                 await ctx.send(f"<@{ctx.author.id}>, This user is already muted.")
                 return

        for role in ctx.guild.roles:
            if role.name.lower().startswith("muted"):
                await member.add_roles(role)
                await ctx.send(f"<@{ctx.author.id}>, You have muted ``{member.display_name}`` until ``{time} CT``")

                logchannel = self.client.get_channel(788321126160924690)
                embed = discord.Embed(
                    title = 'Mute Log',
                    description = f'Mute issued by {ctx.author.display_name} in #{ctx.channel.name}',
                    colour = discord.Colour.purple()
                )

                embed.add_field(name='Victim',value=f"```{member.display_name}```")
                embed.add_field(name='Expiration',value=f"```{time.upper()} CT```")
                embed.add_field(name='Moderator Note',value=f"```{reason}```")

                filedir = "C:/Users/Server/Desktop/wizardBOT/storage/mutes.json"
                with open(filedir) as json_file:
                    userid = member.id
                    data = json.load(json_file)
                    mutedata = data["mutes"]

                    y = {
                        f"{userid}": {
                            "expires": str(time)
                        }
                    }

                    for element in mutedata:
                        if f'{str(userid)}' in element:
                            del element[f'{str(userid)}']

                        with open(filedir, 'w') as data_file:
                            json.dump(mutedata, data_file)

                    mutedata.append(y)
                write_json(data,filedir)


                await logchannel.send(embed=embed)
                gotDM=True
                try:
                    dm = await member.create_dm()
                except Exception as e:
                    gotDM=False
                    print(e)

                embed = discord.Embed(
                    title = f'You have been muted in {ctx.guild.name}',
                    description = f'',
                    colour = discord.Colour.dark_gray()
                )

                embed.add_field(name='Expiration',value=f"```{time.upper()} CT (UTC-06:00)```",inline=False)
                embed.add_field(name='Moderator Note',value=f"```{reason}```",inline=False)
                embed.add_field(name="Links", value=f"[Appeal Form](https://docs.google.com/forms/d/e/1FAIpQLSfZwN69hB8aPs8QtvzqO1LSRvAxxkws13TS6ZeqEf90pXjUMA/viewform?usp=sf_link)\n[Community Guidelines](https://discord.com/guidelines)", inline=False)

                try:
                    await dm.send(embed=embed)
                except Exception:
                    print("couldn't dm")
                await write_modlog(self.client,ctx,member.id,time,"Mute",reason,ctx.author.id)
                return
        return

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, memberidentification, *, reason="No reason provided."):
        member = await returnmember(self.client,ctx, memberidentification)
        userid = member.id
        filedir = "C:/Users/Server/Desktop/wizardBOT/storage/mutes.json"


        try:
            with open(filedir) as json_file:
                mdata = json.load(json_file)
                mutedata = mdata["mutes"]

            for mutedict in mutedata:
                if mutedict.get(str(userid), None):
                    userdata = mutedict[str(userid)]
                    expiredate = userdata["expires"]
                    memid = userid
                    if int(memid) == userid:
                        with open(filedir) as json_file:
                            data = json.load(json_file)
                            mutedata = data["mutes"]

                            for element in mutedata:
                                if f'{str(userid)}' in element:
                                    del element[f'{str(userid)}']

                                with open(filedir, 'w') as data_file:
                                    json.dump(mutedata, data_file)
                                    didTheThing = True

                        write_json(data,filedir)

                        for role in member.roles:
                            if role.name.lower().startswith("muted"):
                                await member.remove_roles(role)

                                await ctx.send(f"<@{ctx.author.id}>, Successfully unmuted ``{member.display_name}``")

                                logchannel = self.client.get_channel(788321126160924690)
                                embed = discord.Embed(
                                    title = 'Unmute Log',
                                    description = f'Unmute issued by {ctx.author.display_name} in #{ctx.channel.name}',
                                    colour = discord.Colour.blurple()
                                )

                                embed.add_field(name='Victim',value=f"```{member.display_name}```")
                                embed.add_field(name='Expiration',value=f"```{expiredate} CT```")
                                embed.add_field(name='Moderator Note',value=f"```{reason}```")

                                await logchannel.send(embed=embed)
                                return
        except Exception as e:
            print(e)
            return

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, memberidentification, *, reason="No reason provided"):
        member = await returnmember(self.client,ctx, memberidentification)
        await write_modlog(self.client,ctx,member.id,"N/A","Warn",reason,ctx.author.id)
        embed = discord.Embed(
            title = f'You have been warned in {ctx.guild.name}',
            description = '',
            colour = discord.Colour.dark_gray()
        )

        embed.add_field(name="Moderator Note", value=f"{reason}", inline=False)
        embed.add_field(name="Links", value=f"[Appeal Form](https://docs.google.com/forms/d/e/1FAIpQLSfZwN69hB8aPs8QtvzqO1LSRvAxxkws13TS6ZeqEf90pXjUMA/viewform?usp=sf_link)\n[Community Guidelines](https://discord.com/guidelines)", inline=False)

        try:
            dm = await member.create_dm()
            await dm.send(embed=embed)
        except Exception:
            print('lol they blocked the bot mad')
        
        await ctx.send(f"<@{ctx.author.id}>, Successfully warned ``{member.display_name}`` ✅")

    @tasks.loop(seconds=10)
    async def mutetick(self):
        await self.client.wait_until_ready()
        global guildid
        guild = self.client.get_guild(guildid)
        now = datetime.now()
        dt_string = now.strftime(f"%m/%d/%Y %I:%M %p")

        filedir = "C:/Users/Server/Desktop/wizardBOT/storage/mutes.json"
        with open(filedir) as json_file:
            data = json.load(json_file)
            mutedata = data["mutes"]

        for mutedict in mutedata:
            for userdict in mutedict:
                userdata = mutedict[str(userdict)]
                
                try:
                    strmemid = str(userdict)
                    memid = int(strmemid)
                except Exception as e:
                    continue
                
                expiredate = userdata["expires"] 
                if expiredate == dt_string:
                    with open(filedir) as json_file:
                        userid = memid
                        data = json.load(json_file)
                        mutedata = data["mutes"]

                        for element in mutedata:
                            if f'{str(userid)}' in element:
                                del element[f'{str(userid)}']

                            with open(filedir, 'w') as data_file:
                                json.dump(mutedata, data_file)
                                didTheThing = True

                    write_json(data,filedir)


                    try:
                        member = guild.get_member(int(memid))
                        for role in member.roles:
                            if role.name.lower().startswith("muted"):
                                await member.remove_roles(role)
                    except Exception as e:
                        print(e)

                    logchannel = self.client.get_channel(788321126160924690)
                    embed = discord.Embed(
                        title = 'Unmute Log',
                        description = f'Unmute issued automatically by expiration time.',
                        colour = discord.Colour.blurple()
                    )

                    embed.add_field(name='Victim',value=f"```{member.display_name}```")
                    embed.add_field(name='Expiration',value=f"```{expiredate} CT```")
                    embed.add_field(name='Moderator Note',value=f"```Mute expired.```")

                    await logchannel.send(embed=embed)
                        
    @tasks.loop(seconds=30)
    async def bantick(self):
        await self.client.wait_until_ready()
        global guildid
        guild = self.client.get_guild(guildid)
        now = datetime.now()
        dt_string = now.strftime(f"%m/%d/%Y %I:%M %p")
        filedir = "C:/Users/Server/Desktop/wizardBOT/storage/bans.json"
        with open(filedir) as json_file:
            bdata = json.load(json_file)
            bandata = bdata["bans"]


        bans = await guild.bans()
        for ban_entry in bans:
            for dictt in bandata:
                if dictt.get(str(ban_entry.user.id), None):
                    userdata = dictt[str(ban_entry.user.id)]

                    expiredate = userdata["expires"]      
                    if expiredate == dt_string:
                        user = await self.client.fetch_user(ban_entry.user.id)

                        with open(filedir) as json_file:
                            userid = ban_entry.user.id
                            data = json.load(json_file)
                            bandata = data["bans"]

                            for element in bandata:
                                if f'{str(userid)}' in element:
                                    del element[f'{str(userid)}']

                                with open(filedir, 'w') as data_file:
                                    json.dump(bandata, data_file)
                                    didTheThing = True

                        write_json(data,filedir)

                        await guild.unban(user)

                        logchannel = self.client.get_channel(788321126160924690)
                        embed = discord.Embed(
                            title = 'Unban Log',
                            description = f'Unban issued automatically by expiration time.',
                            colour = discord.Colour.blurple()
                        )

                        embed.add_field(name='Victim',value=f"```{ban_entry.user.name}```")
                        embed.add_field(name='Expiration',value=f"```{expiredate} CT```")
                        embed.add_field(name='Moderator Note',value=f"```Ban expired.```")

                        await logchannel.send(embed=embed)
                        found = False

    def cog_unload(self):
        self.mutetick.cancel()
        self.bantick.cancel()

#returns member 
async def returnmember(client,ctx, evaluate):
    if evaluate.isdigit():
        try:
            memberuser = ctx.guild.get_member(int(evaluate))
        except Exception as e:
            memberuser = await client.fetch_user(int(evaluate))
        if memberuser:
            return memberuser

    if '#' in evaluate:
        membernametable = evaluate.split('#')

        memberuser = membernametable[0].lower()
        memberdiscrim = membernametable[1]

        for user in ctx.guild.members:
            if memberuser == user.name.lower() or memberuser == user.display_name.lower():
                return user

    if ctx.message.mentions:
        ids = ctx.message.mentions[0].id
        memberuser = ctx.guild.get_member(ids)
        if memberuser:
            return memberuser
    
    for member in ctx.guild.members:
        if member.display_name.lower().startswith(evaluate.lower()) or member.name.lower().startswith(evaluate.lower()):
            return member
    
    return None


async def returndateandreason(ctx, timestring):
    if timestring == None:
        return "1/1/2050 12:00 AM", "No reason provided."
    isArg1 = False
    isArg2 = False
    isArg3 = False
    arg1num = ""
    arg1strid = ""
    arg2num = ""
    arg2strid = ""
    arg3num = ""
    arg3strid = ""
    arg4num = ""
    arg4strid = ""    
    stringtable = timestring.split(' ')

    if stringtable[0].isalpha():
        return timestring,"1/01/2050 12:00 AM"

    currentTime = datetime.now()

    try:
        for character in stringtable[0]:
            if character.isdigit():
                arg1num = arg1num + character
            if character.isalpha():
                arg1strid = arg1strid + character

        if arg1num + arg1strid == stringtable[0] and len(arg1strid) == 1:
            if arg1strid.lower() == "m" or arg1strid.lower() == "min" or arg1strid.lower() == "minute" or arg1strid.lower() == "minutes":
                isArg1 = True
                currentTime = currentTime + timedelta(minutes=int(arg1num)) 
            if arg1strid.lower() == "h" or arg1strid.lower() == "hour" or arg1strid.lower() == "hours":
                isArg1 = True
                currentTime = currentTime + timedelta(hours=int(arg1num))     
            if arg1strid.lower() == "d" or arg1strid.lower() == "day" or arg1strid.lower() == "days":
                isArg1 = True
                currentTime = currentTime + timedelta(days=int(arg1num))                 
            if arg1strid.lower() == "w" or arg1strid.lower() == "week" or arg1strid.lower() == "weeks":
                isArg1 = True
                currentTime = currentTime + timedelta(weeks=int(arg1num))  
            if arg1strid.lower() == "y" or arg1strid.lower() == "year" or arg1strid.lower() == "years":
                isArg1 = True
                currentTime = currentTime + timedelta(days=365 * int(arg1num))  
        else:
            return timestring,"1/01/2050 12:00 AM"

        if stringtable[1]:
            for character in stringtable[1]:
                if character.isdigit():
                    arg2num = arg2num + character
                if character.isalpha():
                    arg2strid = arg2strid + character

            if arg2num + arg2strid == stringtable[1] and len(arg2strid) == 1:
                if arg2strid.lower() == "m" or arg2strid.lower() == "min" or arg2strid.lower() == "minute" or arg2strid.lower() == "minutes":
                    isArg2 = True
                    currentTime = currentTime + timedelta(minutes=int(arg2num))   
                if arg2strid.lower() == "h" or arg2strid.lower() == "hour" or arg2strid.lower() == "hours":
                    isArg2 = True
                    currentTime = currentTime + timedelta(hours=int(arg2num))    
                if arg2strid.lower() == "d" or arg2strid.lower() == "day" or arg2strid.lower() == "days":
                    isArg2 = True
                    currentTime = currentTime + timedelta(days=int(arg2num))                
                if arg2strid.lower() == "w" or arg2strid.lower() == "week" or arg2strid.lower() == "weeks":
                    isArg2 = True
                    currentTime = currentTime + timedelta(weeks=int(arg2num)) 
                if arg2strid.lower() == "y" or arg2strid.lower() == "year" or arg2strid.lower() == "years":
                    isArg2 = True
                    currentTime = currentTime + timedelta(days=365 * int(arg2num)) 


        if stringtable[2]:
            for character in stringtable[2]:
                if character.isdigit():
                    arg3num = arg3num + character
                if character.isalpha():
                    arg3strid = arg3strid + character

            if arg3num + arg3strid == stringtable[2] and len(arg3strid) == 1:
                if arg3strid.lower() == "m" or arg3strid.lower() == "min" or arg3strid.lower() == "minute" or arg3strid.lower() == "minutes":
                    isArg3 = True
                    currentTime = currentTime + timedelta(minutes=int(arg3num))   
                if arg3strid.lower() == "h" or arg3strid.lower() == "hour" or arg3strid.lower() == "hours":
                    isArg3 = True
                    currentTime = currentTime + timedelta(hours=int(arg3num))    
                if arg3strid.lower() == "d" or arg3strid.lower() == "day" or arg3strid.lower() == "days":
                    isArg3 = True
                    currentTime = currentTime + timedelta(days=int(arg3num))                
                if arg3strid.lower() == "w" or arg3strid.lower() == "week" or arg3strid.lower() == "weeks":
                    isArg3 = True
                    currentTime = currentTime + timedelta(weeks=int(arg3num))  
                if arg3strid.lower() == "y" or arg3strid.lower() == "year" or arg3strid.lower() == "years":
                    isArg3 = True
                    currentTime = currentTime + timedelta(days=365 * int(arg3num)) 

        if stringtable[3]:
            for character in stringtable[3]:
                if character.isdigit():
                    arg4num = arg4num + character
                if character.isalpha():
                    arg4strid = arg4strid + character

                    if arg4num + arg4strid == stringtable[3] and len(arg4strid) == 1:
                        await ctx.send(f"<@{ctx.author.id}>, The maximum arguments that can be passed for time is 3.")
                        return None,None
    except Exception as e:
        print(e)

    if isArg1:
        stringtable.remove(stringtable[0])
    if isArg2:
        stringtable.remove(stringtable[0])
    if isArg3:
        stringtable.remove(stringtable[0])

    try:
        reason = " ".join(stringtable)
    except Exception as e:
        print(e)
        reason = "No reason provided."

    try:
        a = currentTime.strftime(f"%m/%d/%Y")
        month,day,year = a.split('/')
        datetime(int(year),int(month),int(day))
    except Exception as e:
        await ctx.send(f"<@{ctx.author.id}>, {e}.")
        return

    return reason, currentTime.strftime(f"%m/%d/%Y %I:%M %p")

#checks if the action member is below the victim member
def isbelowrole(ctx, memberid, compareid):
    memberuser = ctx.guild.get_member(memberid)
    compareuser = ctx.guild.get_member(compareid)

    try:
        if compareuser.top_role >= memberuser.top_role:
            return False
        else:
            return True
    except Exception:
        return False

def write_json(data, filename): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

async def write_modlog(client,ctx,memberid,date,case,reason="No reason provided.",moderatorid=None):
    filedir = "C:/Users/Server/Desktop/wizardBOT/storage/modlogs.json"
    member = await client.fetch_user(int(memberid))
    moderator = ctx.guild.get_member(int(moderatorid))
    caseid = random.randint(1,99999999999999)
    currentTime = datetime.now()
    time = currentTime.strftime(f"%m/%d/%Y %I:%M %p")
    with open(filedir) as json_file:
        userid = memberid
        data = json.load(json_file)
        logdata = data["modlogs"]
        
        y = {
            f"{caseid}": {
                "casetype": str(case),
                "caseid": str(caseid),
                "memberid": str(member.id),
                "modid": str(moderator.id),
                "date": str(date),
                "issdate": str(time),
                "reason": str(reason)
            }
        }

        for element in logdata:
            if f'{str(userid)}' in element:
                del element[f'{str(userid)}']

            with open(filedir, 'w') as data_file:
                json.dump(logdata, data_file)

        logdata.append(y)
    write_json(data,filedir)

def setup(client):
    client.add_cog(Moderation(client))
