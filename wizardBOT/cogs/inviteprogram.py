import discord
import os
from discord.ext import commands
from discord import Intents
import time 
import json
from file_read_backwards import FileReadBackwards
global currentlyEnrolling
currentlyEnrolling = []

class InviteProgram(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def enroll(self, ctx):
        global currentlyEnrolling
        currentlyEnrolling.append(ctx.author.id)
        with open("C:/Users/Server/Desktop/wizardBOT/storage/invite_blacklist.json") as json_file:
            data = json.load(json_file)
            blacklistdata = data["blacklist"]

            try:
                for dictt in blacklistdata:
                    if dictt.get(str(ctx.author.id), None):

                        blacklistdict = dictt[str(ctx.author.id)]
                        blacklistreason = blacklistdict["reason"]
                        await ctx.send(f'<@{ctx.author.id}>, You are blacklisted from the Invite Program under reason: ``{blacklistreason}`` (Cancelled!)')
                        currentlyEnrolling.remove(ctx.author.id)
                        return
            except Exception as e:
                print(e)


        for role in ctx.author.roles:
            for userid in currentlyEnrolling:
                if ctx.author.id == userid:
                    if 'Inviter' in role.name:
                        await ctx.send(f'<@{ctx.author.id}>, You are already enrolled into the invite program. To unenroll, do ;unenroll. (Cancelled!)')
                        currentlyEnrolling.remove(ctx.author.id)
                        return

        await ctx.send(f'<@{ctx.author.id}>, Please respond with the invite you would like to link to your account.')

    @commands.command()
    async def unenroll(self, ctx):
        remove = False
        for role in ctx.author.roles:
           if 'Inviter' in role.name:
                await ctx.author.remove_roles(role)
                remove = True

        if remove == True:
            await ctx.send(f'<@{ctx.author.id}>, Sucessfully removed from the program. (Success!)')
        else:
            await ctx.send(f'<@{ctx.author.id}>, You are not in the invite program.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        goodToGo = False
        global currentlyEnrolling

        for userid in currentlyEnrolling:
            if message.author.id == userid:
                goodToGo = True
                break 
        
        if goodToGo:
            for userid in currentlyEnrolling:
                if message.author.id == userid:
                    if 'https://discord.gg/' in message.content:
                        invites1 = await message.guild.invites()
                        for invite in invites1:
                            if str(invite) == str(message.content):
                                try:
                                    if invite.inviter.id != message.author.id:
                                        await message.channel.send(f'<@{message.author.id}>, You must use your own link. (Cancelled!)')
                                        return
                                    if invite.max_age != 0:
                                        await message.channel.send(f'<@{message.author.id}>, You must use a link that wont expire. (Cancelled!)')
                                        return

                                    filedir = "C:/Users/Server/Desktop/wizardBOT/storage/invite_program.json"
                                    with open(filedir) as json_file:
                                        data = json.load(json_file)
                                        invitedata = data["inviters"]

                                        y = {
                                            f"{userid}": {
                                                "invite": str(invite)
                                            }
                                        }

                                        for element in invitedata:
                                            if f'{str(userid)}' in element:
                                                del element[f'{str(userid)}']

                                            with open(filedir, 'w') as data_file:
                                                json.dump(invitedata, data_file)

                                        invitedata.append(y)
                                    write_json(data,filedir)

                                    await message.channel.send(f'<@{message.author.id}>, You have been successfully enrolled into the invite program! (Success!)')
                                    currentlyEnrolling.remove(message.author.id)

                                    role = discord.utils.get(message.guild.roles, name="Inviter")
                                    await message.author.add_roles(role)

                                    return
                                except Exception as e:
                                    await message.channel.send(f'<@{message.author.id}>, An unexpected error occured: ``{e}`` (Cancelled!)')
                                    currentlyEnrolling.remove(message.author.id)
                                    return
                    else:
                        await message.channel.send(f'<@{message.author.id}>, Please provide the full invite link. (Cancelled!)')
                        currentlyEnrolling.remove(message.author.id)
                        return

    @commands.command(ban_members=True)
    async def iblacklist(self, ctx, memberid, reason="No reason provided."):
        filedir = "C:/Users/Server/Desktop/wizardBOT/storage/invite_blacklist.json"
        userid = memberid
        member = ctx.message.author.guild.get_member(int(userid))

        if member == None:
            await ctx.send(f'``{str(userid)}`` Does not exist in the server. (Cancelled!)')
            return

        with open(filedir) as json_file:
            data = json.load(json_file)
            blacklistdata = data["blacklist"]

            for element in blacklistdata:
                if f'{str(userid)}' in element:
                    await ctx.send(f'``{str(userid)}`` Is already blacklisted, overwriting. (Notice)')
                    del element[f'{str(userid)}']

            with open(filedir, 'w') as data_file:
                json.dump(blacklistdata, data_file)

            y = {
                f"{userid}": {
                    "reason": str(reason)
                }
            }
    
            blacklistdata.append(y)
            write_json(data,filedir)   
            if reason != None:
                await ctx.send(f'``{str(userid)}`` Has successfully been blacklisted from the Invite Program under reason: ``{reason}``. (Success!)')
            else:
                await ctx.send(f'``{str(userid)}`` Has successfully been blacklisted from the Invite Program under reason: ``No reason provided``. (Success!)')
    
    @commands.command(ban_members=True)
    async def uniblacklist(self, ctx, memberid):
        filedir = "C:/Users/Server/Desktop/wizardBOT/storage/invite_blacklist.json"
        didTheThing = False
        userid = memberid
        member = ctx.message.author.guild.get_member(int(userid))

        if member == None:
            await ctx.send(f'``{str(userid)}`` Does not exist in the server. (Cancelled!)')
            return

        with open(filedir) as json_file:
            data = json.load(json_file)
            blacklistdata = data["blacklist"]

            for element in blacklistdata:
                if f'{str(userid)}' in element:
                    del element[f'{str(userid)}']

                with open(filedir, 'w') as data_file:
                    json.dump(blacklistdata, data_file)
                    didTheThing = True

        write_json(data,filedir)

        if didTheThing == True:
            await ctx.send(f"<@{ctx.author.id}>, Successfully unblacklisted ``{str(userid)}`` from the Invite Program. (Success!)")
            return
        else:
            await ctx.send(f"<@{ctx.author.id}>, An error occured or the user is not blacklisted. (Failed!)")
            return

    @commands.Cog.listener()
    async def on_member_join(self,member):
        invitelogchannel = self.client.get_channel(790021675403837490)

        embed = discord.Embed(
            title = 'Inviter Log',
            description = f"``{member.display_name}`` has joined the server",
            colour = discord.Colour.orange()
            )
            
        await invitelogchannel.send(embed=embed)

        with open("C:/Users/Server/Desktop/wizardBOT/storage/invite_program.json") as json_file:
            isInviter1 = False
            isInviter2 = False
            isInviter3 = False

            logchannel = self.client.get_channel(790021675403837490)
            data = json.load(json_file)
            invitedata = data["inviters"]
            user = False

            try:
                for dictt in invitedata:
                    for mem in member.guild.members:
                        if dictt.get(str(mem.id), None):
                            userid = int(mem.id)
                            user = member.guild.get_member(userid)
                            invitedict = dictt[str(userid)]
                            invitelink = invitedict["invite"]

                            for role in user.roles:
                                
                                if 'Inviter' in role.name:
                                    invites1 = await member.guild.invites()
                                    for invite in invites1:
                                        if str(invite) == str(invitelink):
                                            for role in user.roles:
                                                if role.name == 'Inviter I':
                                                    isInviter1 = True
                                                if role.name == 'Inviter II':
                                                    isInviter2 = True
                                                if role.name == 'Inviter III':
                                                    isInviter3 = True

                                            if isInviter1 == False:
                                                if invite.uses >= 5:
                                                    role = discord.utils.get(user.guild.roles, name="Inviter I")
                                                    await user.add_roles(role)

                                                    embed = discord.Embed(
                                                        title = 'Inviter Advancement',
                                                        description = f'``{user.display_name}`` has advanced to Inviter I',
                                                        colour = discord.Colour.green()
                                                    )
                                                    await logchannel.send(embed=embed)
                                            if isInviter2 == False:
                                                if invite.uses >= 10:
                                                    role = discord.utils.get(user.guild.roles, name="Inviter II")
                                                    await user.add_roles(role)

                                                    embed = discord.Embed(
                                                        title = 'Inviter Advancement',
                                                        description = f'``{user.display_name}`` has advanced to Inviter II',
                                                        colour = discord.Colour.green()
                                                    )
                                                    await logchannel.send(embed=embed)
                                            if isInviter3 == False:
                                                if invite.uses >= 20:
                                                    role = discord.utils.get(user.guild.roles, name="Inviter III")
                                                    await user.add_roles(role)

                                                    embed = discord.Embed(
                                                        title = 'Inviter Advancement 🏆',
                                                        description = f'``{user.display_name}`` has advanced to Inviter III',
                                                        colour = discord.Colour.green()
                                                    )
                                                    await logchannel.send(embed=embed)
            except Exception as e:
                print("exception:", e)
                pass

def write_json(data, filename): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

def setup(client):
    client.add_cog(InviteProgram(client))