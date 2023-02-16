import random

import discord
from discord.ext import commands


class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Short Input"))
        self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])


class Users(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description='Получить случайное число')
    async def roll(self, ctx, argmin: int = 0, argmax: int = 100):
        if argmin >= argmax or argmin < 0:
            return await ctx.respond('Нормально границы поставь. Пример - %ролл 60 100 или просто %ролл')
        embed = discord.Embed(
            description=f'{ctx.author.mention} выбросил **{random.randint(argmin, argmax)}** из {argmin}'
                        f' - {argmax}',
            color=ctx.author.top_role.colour)
        await ctx.respond(embed=embed)

    # @commands.command(
    #     brief='Посмотреть чей-то аватар',
    #     help='Посмотреть чей-то аватар, пинганув его или указав ID. '
    #          'Если не пинговать, то покажется аватар того, кто вызвал команду.',
    #     usage='%avatar (пинг пользователся)'
    # )
    @discord.slash_command(description='Посмотреть чей-то аватар')
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:  # if member is no mentioned
            member = ctx.author
        if type(member) is int:
            try:
                member = ctx.guild.get_member(member)
            except:
                return
        userAvatar = member.display_avatar.url
        if member.nick is None:
            member.nick = member
        embed = discord.Embed(title=f'Аватар {member.nick}', color=member.top_role.colour)
        embed.set_image(url=userAvatar)
        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def modal_slash(self, ctx: discord.ApplicationContext):
        """Shows an example of a modal dialog being invoked from a slash command."""
        modal = MyModal(title="Modal via Slash Command")
        await ctx.send_modal(modal)

    # @commands.Cog.listener()  # event listeners
    # async def on_member_join(self, member):
    #     # you must enable the proper intents
    #     # to access this event.
    #     # See the Popular-Topics/Intents page for more info
    #     await member.send('Welcome to the server!')


def setup(bot):
    bot.add_cog(Users(bot))
