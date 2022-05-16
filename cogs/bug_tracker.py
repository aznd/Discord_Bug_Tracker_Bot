import discord
import logging
from discord.ext import commands


class BugTracker(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role("Dev")
    async def add_bug(
        self, ctx: discord.ext.commands.Context, title=None, description=None
    ):
        channel = self.client.get_channel(974701727783735367)
        if title is None or description is None:
            await ctx.send(
                '''You need to provide a title and a description of the bug!\n
                    Use the following format: !bugadd "titlehere" "descriptionhere"'''
            )
            return
        embed = embed = discord.Embed(title=title, description=description)
        message = await channel.send(embed=embed)
        await message.create_thread(name=title)

    @commands.command(aliases=["reopen_bug"])
    @commands.has_role("Dev")
    async def close_bug(self, ctx: discord.ext.commands.Context):
        thread = ctx.channel
        if type(thread) == discord.Thread:
            if thread.archived:
                await thread.edit(archived=False)
                await ctx.send("Bug has been re-opened.")
            elif not thread.archived:
                await thread.edit(archived=True, locked=True)
                await ctx.send("Bug has been closed.")
        else:
            await ctx.send("This command can only be used in a thread.")


async def setup(client):
    await client.add_cog(BugTracker(client))
