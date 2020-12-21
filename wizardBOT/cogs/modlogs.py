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


class ModLogs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def modlogs(self,ctx, memberidentification):
        hasLogs = False
        stop = False
        casenum = 0
        fields = 0
        member = await returnmember(self.client,ctx,memberidentification)

        if member:
            filedir = "C:/Users/Server/Desktop/wizardBOT/storage/modlogs.json"
        else:
            await ctx.send(f"<@{ctx.author.id}>, Couldn't find ``{memberidentification}``")
            return

        with open(filedir) as json_file:
            mdata = json.load(json_file)
            logdata = mdata["modlogs"]

        embed = discord.Embed(
            title = f"{member.name}'s Moderation Logs",
            description = f'',
            colour = discord.Colour.blue()
        )      

        for logdictt in logdata:
            for logdict in logdictt:
                logdict = logdictt[str(logdict)]
                try:
                    casetype = logdict["casetype"]
                    caseid = logdict["caseid"]
                    memberid = logdict["memberid"]
                    modid = logdict["modid"]
                    date = logdict["date"]
                    issdate = logdict["issdate"]
                    reason = logdict["reason"]
                    moderator = ctx.guild.get_member(int(modid))
                except Exception as e:
                    print("Exception: " + e)

                if int(memberid) == member.id:
                    hasLogs = True
                    casenum = casenum + 1
                    for field in embed.fields:
                        fields = fields + 1
                        if fields >= 25:
                            await ctx.send(embed=embed)
                            fields = 0
                            stop = True
                    if stop:
                        stop = False
                        index=0
                        for field in embed.fields:
                            index = index + 1
                            embed.remove_field(index)
                    else:
                        embed.add_field(name=f"Case #{caseid} Log #{casenum}",value=f"```\nCASETYPE: {casetype}\nVICTIM: {member.display_name}:{member.id}\nMODERATOR: {moderator.display_name}:{moderator.id}\nDATE: {date}\nISSDATE: {issdate}\nREASON: {reason}```")

        if hasLogs == False:
            await ctx.send(f"<@{ctx.author.id}>, ``{member.display_name}`` does not have any moderation logs.")
            return
        if fields <=25 and hasLogs:
            await ctx.send(embed=embed)
            hasLogs = False
            fields = 0

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changelogvalue(self, ctx, ID, value, * ,newvalue):
        if value == ID:
            ctx.send(f"<@{ctx.author.id}>, You cannot change the ID of a modlog!")

        with open("C:/Users/Server/Desktop/wizardBOT/storage/modlogs.json") as json_file:
            data = json.load(json_file)
            moddata = data["modlogs"]

            for dictt in moddata:
                if dictt.get(ID, None):
                    moddict = dictt[ID]
                    if moddict[value]:
                        moddict[value] = newvalue
                        with open("C:/Users/Server/Desktop/wizardBOT/storage/modlogs.json", 'w') as file:
                            json.dump(data, file, indent=4)

                        await ctx.send(f"<@{ctx.author.id}>, Successfully changed value and updated modlog.")
                        return    

            await ctx.send(f"<@{ctx.author.id}>, An error occued while matching ID ``{ID}``. If the ID is correct, it's possible value `{value}` doesnt exist.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def deletelog(self, ctx, logid):
        filedir = "C:/Users/Server/Desktop/wizardBOT/storage/modlogs.json"
        with open(filedir) as json_file:
            ldata = json.load(json_file)
            logdata = ldata["modlogs"]


        for logdict in logdata:
            if logdict.get(str(logid), None):
                userdata = logdict[str(logid)]

                with open(filedir) as json_file:
                    data = json.load(json_file)
                    moddata = data["modlogs"]

                    for element in moddata:
                        if f'{str(logid)}' in element:
                            del element[f'{str(logid)}']

                        with open(filedir, 'w') as data_file:
                            json.dump(moddata, data_file)
                            didTheThing = True

                write_json(data,filedir)
                await ctx.send(f"<@{ctx.author.id}>, Successfully removed case ``{logid}`` from log.")
                return
        await ctx.send(f"<@{ctx.author.id}>, Couldn't find case id ``{logid}``. Check the ID and try again.")

def write_json(data, filename): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

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

def setup(client):
    client.add_cog(ModLogs(client))