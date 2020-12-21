import discord
import os
from discord.ext import commands
import time 
import contextlib
import io

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    async def dm(self, ctx, memberid, *, message):
        
        user = self.client.get_user(int(memberid))
        await user.create_dm()
        await user.dm_channel.send(f'{ctx.author.name}: {message}')
        await ctx.message.delete()


    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def say(self,ctx, *, message):
        await ctx.send(message)
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def eval(self,ctx, *, code):
        str_obj = io.StringIO() #Retrieves a stream of data
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        except Exception as e:
            return await ctx.send(f"```{e.__class__.__name__}: {e}```")
        await ctx.send(f'```{str_obj.getvalue()}```')



def setup(client):
    client.add_cog(Fun(client))
