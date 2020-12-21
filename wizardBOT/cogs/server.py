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

global messages
messages = 0
global deletions
deletions = 0
global edits
edits = 0
global joins
joins = 0
global leaves
leaves = 0


class Server(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.resetStats.start()


    @commands.command()
    async def serverstats(self, ctx):
        botmembers = 0
        members = 0 
        for member in ctx.guild.members:
            members = members + 1
            if member.bot:
                botmembers = botmembers + 1


        embed = discord.Embed(
            title = 'Hourly Statistics',
            description = f'',
            colour = discord.Colour.blue()
        )

        embed.add_field(name='Total Members',value=f"{str(members)}")
        embed.add_field(name='Total Bot Members',value=f"{str(botmembers)}")
        embed.add_field(name='Joins',value=f"{str(joins)}")
        embed.add_field(name='Leaves',value=f"{str(leaves)}")
        embed.add_field(name='Messages Sent',value=f"{str(messages)}")
        embed.add_field(name='Messages Deleted',value=f"{str(deletions)}")
        embed.add_field(name='Messages Edited',value=f"{str(edits)}")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)

    @commands.command()
    async def whois(self,ctx,memberidentification):
        user = await returnmember(self.client,ctx,memberidentification) 
        isInServer = False

        if user:
            embed = discord.Embed(
                title = f'{user.name}#{user.discriminator}',
                description = f'{user.mention}',
                colour = discord.Colour.blue()
            )

            for a in ctx.guild.members:
                if a.id == user.id:
                    member = a
                    isInServer = True
                    break
            

            embed.timestamp = datetime.now()
            embed.add_field(name="Server Member Status",value=f"{str(isInServer)}")
            if isInServer:
                try:
                    date = member.joined_at
                    joinedat = date.strftime(f"%A, %B %d %Y @ %H:%M:%S %p")
                except Exception as e:
                    joinedat = "Couldn't find date"
                    print(e)
                date = member.created_at
                createdat = date.strftime(f"%A, %B %d %Y @ %H:%M:%S %p")
                try:
                    date = member.premium_since
                    boosted = date.strftime(f"%A, %B %d %Y @ %H:%M:%S %p")
                except Exception as e:
                    boosted = "User is not a booster"
                    print(e)
                    
                roletable = []

                for role in member.roles:
                    roletable.append(role.mention)

                roles = " ".join(roletable)
                embed.add_field(name="Display Name",value=f"{str(member.display_name)}")
                embed.add_field(name="Joined Server",value=f"{str(joinedat)}")
                embed.add_field(name="Account Created",value=f"{str(createdat)}")
                embed.add_field(name="Booster Since",value=f"{str(boosted)}")
                embed.add_field(name="Roles",value=f"{str(roles)}")
                embed.add_field(name="Status",value=f"{str(member.status)}")
                embed.add_field(name="On Mobile",value=f"{str(member.is_on_mobile())}")
                embed.set_thumbnail(url=member.avatar_url)

            await ctx.send(embed=embed)
            return
        await ctx.send(f"<@{ctx.author.id}>, Couldn't find ``{memberidentification}``")

                
                        

    @tasks.loop(seconds=3600)
    async def resetStats(self):
        await self.client.wait_until_ready()
        global messages
        messages = 0
        global deletions
        deletions = 0
        global edits
        edits = 0
        global joins
        joins = 0
        global leaves
        leaves = 0
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        global deletions
        deletions = deletions + 1
    @commands.Cog.listener()
    async def on_message(mself, message):
        if message.author.bot:
            return
        global messages
        messages = messages + 1
    @commands.Cog.listener()
    async def on_message_edit(self,before,after):
        if after.author.bot:
            return
        global edits
        edits = edits + 1
    @commands.Cog.listener()
    async def on_member_join(self,member):
        global joins
        joins = joins + 1
    @commands.Cog.listener()
    async def on_member_leave(self,message):
        global leaves
        leaves = leaves + 1

def write_json(data, filename): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

def returnmember(ctx, evaluate):
    if evaluate.isdigit():
        memberuser = ctx.guild.get_member(int(evaluate))
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
    client.add_cog(Server(client))