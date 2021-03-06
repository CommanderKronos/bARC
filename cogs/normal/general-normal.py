""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import json
import os
import platform
import random
import sys

import aiohttp
import disnake
from disnake.ext import commands
from disnake.ext.commands import Context
from pprint import pprint
from datetime import date

from helpers import checks
from helpers import sqlite as sql
from helpers import bgsapi as bgs
from modules.flags import sysflags

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class General(commands.Cog, name="general-normal"):
    def __init__(self, bot):
        if "data" not in os.listdir():
            os.mkdir("data")
        self.conn, self.cursor = sql.create_conn(os.getcwd() + r"\data\bARC.db")
        self.bot = bot

    @commands.command(
        name="flagtest"
    )
    @checks.not_blacklisted()
    async def flagtest(self, context: Context, *, flags: sysflags.BasicFlags):
        # print(flags.get_flags())
        for flag in flags.get_flags():
            print(flags.get_flags()[flag])
        print(flags.test)
        print(flags.cringe)
        print(flags.based)

    @commands.group(
        name="bgsget"
    )
    async def bgsget(self, context: Context):
        if context.invoked_subcommand is None:
            await context.send("bgs get what?")

    @bgsget.command(
        name="system"
    )
    @checks.not_blacklisted()
    async def bgsget_system(self, context: Context, *args):
        if len(args) == 1:
            result = bgs.basic_system_lookup(args[0])
            embed = disnake.Embed(
                title="Search Result:"
            )
            content = "System_id: {}\n" \
                      "EDDB_id: {}\n" \
                      "X Coord: {}\n" \
                      "Y Coord: {}\n" \
                      "Z Coord: {}\n".format(result['system_id'], result['eddbid'], result['x'],
                                             result['y'], result['z'])
            embed.add_field(
                name=result['name'],
                value=content
            )
        else:
            embed = disnake.Embed()
            valid_params, param = bgs.validate_sys_params(args)
            if valid_params:
                pass
        await context.send(embed=embed)

    @commands.command(
        name="previoustick",
        decription="Get data of the previous tick"
    )
    @commands.has_role(938412271665827891)
    async def previoustick(self, context: Context) -> None:
        """
        Get data of the previous tick
        """
        print(bgs.getprevioustick())

    @commands.command(
        name="lasttick",
        decription="Get data of the most recent tick"
    )
    @commands.has_role(938412271665827891)
    async def lasttick(self, context: Context) -> None:
        """
        Get data of the most recent tick
        """
        print(bgs.getlasttick())

    @commands.command(
        name="bgsreport",
        description="Get a bgsreport from the elitebgs api"
    )
    @commands.has_role(938412271665827891)
    async def bgsreport(self, context: Context) -> None:
        """
        Get a bgs report from the elitebgs api
        """
        data, conflicts = bgs.bgsreport()
        for system in data.keys():
            embed = disnake.Embed(
                title="BGSReport of {} / {}".format(system, date.today())
            )
            # if conflicts[system]:
            #     bgs.conflict_pic_gen(conflicts[system], system)
            #     embed.set_image(file=disnake.File("temp/conflicttable.png"))

            for factiondict in data[system]:
                # Double down: \U000023EC   # Double excla: \U0000203C
                # Double up: \U000023EB     # Green tick: \U00002705
                # Down: \U0001F53D          # Excla: \U00002757
                # Up: \U0001F53C            # Blue tick: \U00002611

                if factiondict['infchange'] <= -0.05:
                    infchange = "{0:.2%}".format(factiondict['infchange']) + '\U0000203C'
                elif factiondict['infchange'] >= 0.05:
                    infchange = "{0:.2%}".format(factiondict['infchange']) + '\U00002705'
                elif factiondict['infchange'] < 0.0:
                    infchange = "{0:.2%}".format(factiondict['infchange']) + '\U00002757'
                elif factiondict['infchange'] > 0.0:
                    infchange = "{0:.2%}".format(factiondict['infchange']) + '\U00002611'
                else:
                    infchange = "{0:.2%}".format(factiondict['infchange'])

                content = "Influence: {}, Change: {}\n" \
                          "Active states:      {}\n" \
                          "Pending states:     {}\n" \
                          "Recovering states:  {}\n".format("{0:.2%}".format(factiondict['influence']),
                                                            infchange,
                                                            ", ".join(factiondict['active']),
                                                            ", ".join(factiondict['pending']),
                                                            ", ".join(factiondict['recovering']))
                embed.add_field(
                    name=factiondict['name'],
                    value=content,
                    inline=False
                )
            await context.send(embed=embed)

    @commands.command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    @checks.not_blacklisted()
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.
        :param context: The context in which the command has been executed.
        """
        embed = disnake.Embed(
            description="Used [Krypton's](https://krypt0n.co.uk) template, this bot was developed for the use in the "
                        "ARRC Discord server for squadron management. (And to stage a coup)",
            color=0x6800B6
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Owner:",
            value="CommanderKronos#5555",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {config['prefix']} for normal commands",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {context.author}"
        )
        await context.send(embed=embed)

    @commands.command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.
        :param context: The context in which the command has been executed.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = disnake.Embed(
            title="**Server Name:**",
            description=f"{context.guild}",
            color=0x9C84EF
        )
        embed.set_thumbnail(
            url=context.guild.icon.url
        )
        embed.add_field(
            name="Server ID",
            value=context.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=context.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {context.guild.created_at}"
        )
        await context.send(embed=embed)

    @commands.command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.
        :param context: The context in which the command has been executed.
        """
        embed = disnake.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    @checks.not_blacklisted()
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.
        :param context: The context in which the command has been executed.
        """
        embed = disnake.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&scope=bot+applications.commands&permissions={config['permissions']}).",
            color=0xD75BF4
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except disnake.Forbidden:
            await context.send(embed=embed)

    @commands.command(
        name="server",
        description="Get the invite link of the discord server of the bot for some support.",
    )
    @checks.not_blacklisted()
    async def server(self, context: Context) -> None:
        """
        Get the invite link of the discord server of the bot for some support.
        :param context: The context in which the command has been executed.
        """
        embed = disnake.Embed(
            description=f"Join the support server for the bot by clicking [here](https://discord.gg/mTBrXyWxAF).",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except disnake.Forbidden:
            await context.send(embed=embed)

    @commands.command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    @checks.not_blacklisted()
    async def eight_ball(self, context: Context, *, question: str) -> None:
        """
        Ask any question to the bot.
        :param context: The context in which the command has been executed.
        :param question: The question that should be asked by the user.
        """
        answers = ["It is certain.", "It is decidedly so.", "You may rely on it.", "Without a doubt.",
                   "Yes - definitely.", "As I see, yes.", "Most likely.", "Outlook good.", "Yes.",
                   "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                   "Cannot predict now.", "Concentrate and ask again later.", "Don't count on it.", "My reply is no.",
                   "My sources say no.", "Outlook not so good.", "Very doubtful."]
        embed = disnake.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0x9C84EF
        )
        embed.set_footer(
            text=f"The question was: {question}"
        )
        await context.send(embed=embed)

    @commands.command(
        name="bitcoin",
        description="Get the current price of bitcoin.",
    )
    @checks.not_blacklisted()
    async def bitcoin(self, context: Context) -> None:
        """
        Get the current price of bitcoin.
        :param context: The context in which the command has been executed.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript")  # For some reason the returned content is of type JavaScript
                    embed = disnake.Embed(
                        title="Bitcoin price",
                        description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
                        color=0x9C84EF
                    )
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
