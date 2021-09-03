""""
Copyright © Samurai 2021 - https://github.com/OsamuraiO
Support server - https://discord.gg/D5pp6cuMah

Description:
This is a template to create your own discord bot in python.
`Please do not delete developer introductions`

Commands :
    ▪ info
    ▪ 8ball
    ▪ ping
    ▪ kick
    ▪ ban
    ▪ clear


Version: 1.3
"""

### import modules
try:
    import discord
    from discord.ext import commands
except:
    print("'discord' module not installed !")
    input("press enter ....")
    exit()
from asyncio import *
import random

### Bot Config
class CONFIG:
    TOKEN = "YourBotToken" # Insert your bot token here
    PREFIX = "Prefix" # Specify your bot prefix, like: ( ! , - )

### Create Bot
client = commands.Bot(command_prefix=CONFIG.PREFIX)

### Bot event
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{CONFIG.PREFIX}help"))
    print("Bot Connected !")

### Commands
client.remove_command('help') # Remove default "help" command
@client.command(aliases=['help','Help','HELP'])
async def bothelp(ctx):

    """
    Send complete list of bot commands to users
    command : help
    """

    embed = discord.Embed(
        title="Help",
        description="***all bot commands***",
        colour=0x0dbaff,
    )
    embed.add_field(
        name="👥 **General** 👥",
        value="```\ninfo\n8ball\nping```",
        inline=True,
    )
    embed.add_field(
        name="⚙ **Admin** ⚙",
        value="```\nkick\nban\nclear```",
        inline=True,
    )
    embed.add_field(
        name="🤖 **Bot Prefix** 🤖",
        value=f"```{CONFIG.PREFIX}```",
        inline=False,
    )
    embed.set_footer(
        text=f"Requested by {ctx.message.author}"
    )
    await ctx.send(embed=embed)

@client.command()
async def info(ctx):

    """
    Send bot and developer information 
    command : info
    """

    embed = discord.Embed(
        title="Info",
        description="Bot information",
        colour=0x0dbaff,
    )
    embed.add_field(
        name="Bot Version",
        value="```v1.3```",
        inline=True,
    )
    embed.add_field(
        name="Bot Prefix",
        value=f"```{CONFIG.PREFIX}```",
        inline=True,
    )
    embed.add_field(
        name="Bot permissions",
        value="```Administrator```",
        inline=True,
    )
    embed.add_field(
        name="Owner",
        value="<@581004762271711252>",
        inline=True,
    )
    embed.add_field(
        name="Bot ID",
        value="```883054286391619634```",
        inline=True,
    )
    embed.add_field(
        name="official Server",
        value="https://discord.gg/D5pp6cuMah",
        inline=True,
    )
    embed.add_field(
        name="Source",
        value="github.com",
        inline=True,
    )
    await ctx.send(embed=embed)

@client.command(aliases=['8ball'])
async def eightball(ctx):

    """
    Question answer with bot, for fan
    # 8Ball
    command : 8ball text
    """

    javab = ['Yes','No']
    embed = discord.Embed(
        title=random.choice(javab),
        colour=0x0dbaff,
    )
    embed.set_footer(
        text=f"Requested by {ctx.message.author}"
    )
    await ctx.send(embed=embed)

@client.command()
async def kick(ctx, member: discord.Member, *args):

    """
    kick a user from the server
    # Requires admin permissions
    command : kick @user#0000 reason
    """

    if ctx.message.author.guild_permissions.kick_members:
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Error!",
                description="User has Admin permissions.",
                colour=0x0dbaff
            )
            await ctx.send(embed=embed)
        else:
            try:
                reason = " ".join(args)
                embed = discord.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{ctx.message.author}**!",
                    colour=0x0dbaff
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await member.kick(reason=reason)
                await ctx.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{ctx.message.author}**!\nReason: {reason}"
                    )
                except:
                    pass
            except:
                embed = discord.Embed(
                    title="Error!",
                    description="An error occurred while trying to kick the user.",
                    colour=0x0dbaff
                )
                await ctx.message.channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Error!",
            description="You don't have the permission to use this command.",
            colour=0x0dbaff
        )
        await ctx.send(embed=embed)

@client.command()
async def ping(ctx):

    """
    Get user latency by bot
    command : ping
    """

    embed = discord.Embed(
        title=f"⏱ Ping : {round(client.latency * 100)}ms",
        colour=0x0dbaff
    )
    embed.set_footer(
        text=f"Requested by {ctx.message.author}"
    )
    await ctx.trigger_typing()
    await ctx.send(embed=embed)

@client.command()
async def ban(ctx, member: discord.Member, *args):

    """
    ban a user from the server
    # Requires admin permissions
    command : ban @user#0000 reason
    """

    if ctx.message.author.guild_permissions.administrator:
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Error!",
                description="User has Admin permissions.",
                colour=0x0dbaff
            )
            await ctx.send(embed=embed)
        else:
            reason = " ".join(args)
            embed = discord.Embed(
                title="User Banned!",
                description=f"**{member}** was banned by **{ctx.message.author}**!",
                colour=0x0dbaff
            )
            embed.add_field(
                name="Reason:",
                value=reason
            )
            embed_message = await ctx.send(embed=embed)
            await member.ban(reason=reason)
            await member.send(f"You were banned by **{ctx.message.author}**!\nReason: {reason}")
            await embed_message.add_reaction("⛔")
    else:
        embed = discord.Embed(
            title="Error!",
            description="You don't have the permission to use this command.",
            colour=0x0dbaff
        )
        await ctx.send(embed=embed)


@client.command()
async def clear(ctx, number='10'):

    """
    Clear server messages
    # Requires admin permissions
    command : clear number
    """

    if ctx.message.author.guild_permissions.administrator:
        number = int(number)
        purged_messages = await ctx.message.channel.purge(limit=number+1)
        embed = discord.Embed(
            title=f"🧹 {ctx.message.author} cleared '{len(purged_messages)}' messages ! 🧹",
            colour=0x0dbaff,
        )
        await ctx.send(embed=embed,delete_after=2)
    else:
        embed = discord.Embed(
            title="Error!",
            description="You don't have the permission to use this command.",
            colour=0x0dbaff
        )
        await ctx.send(embed=embed)

client.run(CONFIG.TOKEN)
