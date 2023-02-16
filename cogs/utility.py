import discord
from discord.ext import commands


# async def addemoji(emoji, message):
#     await message.add_reaction(emoji)
#
#
# async def addrole(roleid, target):
#     rolename = discord.utils.get(target.guild.roles, id=roleid)
#     await target.add_roles(rolename)
#
#
# async def removerole(roleid, target):
#     rolename = discord.utils.get(target.guild.roles, id=roleid)
#     await target.remove_roles(rolename)


# async def check_channel(ctx):
#     if ctx.channel.id == 861923799443177472:
#         return True
#     else:
#         return False


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.command(
    #     aliases=['хелп', 'помощь'],
    #     brief='Показать это сообщение',
    #     help='Увидеть список доступных команд или описание команды, указав её название.',
    #     usage='%[хелп, помощь, help] (название команды)'
    # )
    # async def help(self, ctx, commandname=None):
    #     await ctx.message.delete()
    #     cogs = [c for c in self.bot.cogs.keys()]
    #     cogs.remove('Event')
    #     cogs.remove('Server')
    #     embed = discord.Embed(title='Помощь', color=discord.Colour.random())
    #     if commandname is None:
    #         for cog in cogs:
    #             commands = ''
    #             for command in self.bot.get_cog(cog).walk_commands():
    #                 commands += f'**{command}** - {command.brief}\n'
    #             embed.add_field(name=f'{cog}:', value=f'{commands}', inline=False)
    #         embed.add_field(name='Описание команды:',
    #                         value='Чтобы увидеть полное описание команды, используйте\n**%хелп (название команды)**',
    #                         inline=False)
    #     else:
    #         command = self.bot.get_command(commandname)
    #         try:
    #             embed.add_field(name=f'{str(command).capitalize()}:', value=f'{command.help}\n\n**{command.usage}**')
    #         except AttributeError:
    #             return await ctx.send(f'Команды {commandname} нет.', delete_after=8)
    #     message = await ctx.send(embed=embed)
    #     await message.add_reaction('❌')
    #
    #     def check(reaction, user):
    #         return user.id != 757639306721362111 and str(reaction.emoji) == '❌'
    #
    #     reaction, user = await self.bot.wait_for('reaction_add', check=check)
    #     await message.delete()

    # @commands.command(
    #     brief='Отправить в канал от имени бота сообщение',
    #     help='Отправить в канал от имени бота сообщение. Канал можно указать как ID, так и его пингом.',
    #     usage='%announce (ID канала/пинг канала) [сообщение]'
    # )
    @commands.has_permissions(administrator=True)
    @discord.slash_command(description='Отправить в канал сообщение от имени бота')
    async def announce(self, ctx, channelan, announce_text: str):
        if ctx.author.guild_permissions.administrator:
            if channelan.isdigit():
                await self.bot.get_channel(int(channelan)).send(announce_text)

            else:
                channelan = int(channelan[2:20])
                await self.bot.get_channel(channelan).send(announce_text)

            await ctx.respond('✅', delete_after=5)

    # @commands.command(
    #     brief='Спам-команда',
    #     help='Команда для того, чтобы кого-то заспамить пингами. Или заспамить канал сообщением. Доступна не всем.',
    #     usage='%spam (кол-во отправки сообщения) [сообщение]'
    # )
    @commands.is_owner()
    @discord.slash_command(description='Заставить кого-то страдать')
    async def spam(self, ctx, number: int, spam_text: str):
        for _ in range(number):
            await ctx.send(spam_text)  # " ".join(x for x in args),


def setup(bot):
    bot.add_cog(Utility(bot))
