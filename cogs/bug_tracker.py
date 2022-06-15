import discord
from discord.ext import commands
import bot_config

bug_channel_id = bot_config.bugs_channel_id


class BugTracker(commands.Cog):
    def __init__(self, client):
        self.client: discord.Client = client

    @commands.command()
    @commands.has_role("Dev")
    async def create(
        self,
        ctx: discord.ext.commands.Context,
        title=None,
    ):
        if not ctx.message.reference:
            await ctx.send("You can only use this command in a reply.")
            return
        else:
            channel = self.client.get_channel(bug_channel_id)
            if title is None:
                await ctx.send(
                    '''You need to provide a title and a description of the bug!\n
                        Use the following format: !bugadd "titlehere" "descriptionhere"'''
                )
                return
            thread = await ctx.message.create_thread(name=title)
            embed = discord.Embed(
                title=title,
                description=f"Jump to thread: https://discord.com/channels/{ctx.guild.id}/{thread.id}",
                color=0x38A493,
            )
            await channel.send(embed=embed)

    @commands.command()
    @commands.has_role("Dev")
    async def close(self, ctx: discord.ext.commands.Context):
        thread = ctx.channel
        is_match = False
        if type(thread) == discord.Thread:
            channel = self.client.get_channel(bug_channel_id)

            async for message in channel.history():
                if str(thread.id) in message.embeds[0].description:

                    """
                    If the current thread id is in the description of the embed,
                    e.g.
                    """
                    is_match = True
                    old_title = message.embeds[0].title
                    old_description = message.embeds[0].description
                    await message.delete()
                    if "- CLOSED" in old_title:
                        old_title = old_title.replace(" - CLOSED", "")
                    new_embed = discord.Embed(
                        title=f"{old_title} - CLOSED",
                        description=old_description,
                        color=0xCC7A94,
                    )
                    await channel.send(embed=new_embed)
                    break
            if not is_match:
                await ctx.send(
                    "Could not find bugs in #dev-bugs! Please edit manually."
                )
                return
            await ctx.send("Bug has been closed.")
            await thread.edit(archived=True, locked=True)
        else:
            await ctx.send("This command can only be used in a thread.")

    @commands.command()
    @commands.has_role("Dev")
    async def reopen(self, ctx):
        thread = ctx.channel
        if type(thread) == discord.Thread:
            channel = self.client.get_channel(bug_channel_id)
            async for message in channel.history():
                if str(thread.id) in message.embeds[0].description:
                    title = str(message.embeds[0].title).replace(" - CLOSED", "")
                    old_description = message.embeds[0].description
                    await message.delete()
                    new_embed = discord.Embed(
                        title=title, description=old_description, color=0x38A493
                    )
                    await channel.send(embed=new_embed)
                    await ctx.send("Bug has been re-opened.")
                else:
                    await ctx.send(
                        "Could not find bugs in #dev-bugs! Please edit manually."
                    )
        else:
            await ctx.send("This command can only be used in a thread.")


async def setup(client):
    await client.add_cog(BugTracker(client))
