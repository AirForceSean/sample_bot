import os
from time import strftime, localtime

import discord
from discord.ext import commands

bot = discord.Bot()


@bot.command(description='Проверка работоспособности бота')
async def ping(ctx):
    await ctx.respond('pong!', delete_after=5)


# create Slash Command group with bot.create_group  # Группирование команд
# greetings = bot.create_group("greetings", "Greet people")
#
#
# @greetings.command()
# async def hello(ctx):
#     await ctx.respond(f"Hello, {ctx.author}!")
#
#
# @greetings.command()
# async def bye(ctx):
#     await ctx.respond(f"Bye, {ctx.author}!")


# async def get_animal_types(ctx: discord.AutocompleteContext):  # Список возможных вариантов аргументов команды
#     """
#     Here we will check if 'ctx.options['animal_type']' is
#     and check if it's a marine or land animal and return specific option choices
#     """
#     animal_type = ctx.options['animal_type']
#     if animal_type == 'Marine':
#         return ['Whale', 'Shark', 'Fish', 'Octopus', 'Turtle']
#     else:  # is land animal
#         return ['Snake', 'Wolf', 'Lizard', 'Lion', 'Bird']
#
#
# @bot.slash_command(name="animal")
# async def animal_command(ctx: discord.ApplicationContext,
#                          animal_type: discord.Option(str, choices=['Marine', 'Land']),
#                         animal: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_animal_types))):
#     await ctx.respond(f'You picked an animal type of `{animal_type}` that led you to pick `{animal}`!')


# class MyView(discord.ui.View):  # Create a class called MyView that subclasses discord.ui.View
#     @discord.ui.button(label="Button 1", row=0, style=discord.ButtonStyle.primary)
#     async def first_button_callback(self, button_obj, interaction):
#         await interaction.response.send_message("You pressed me!")
#
#     @discord.ui.button(label="Button 2", row=1, style=discord.ButtonStyle.primary)
#     async def second_button_callback(self, button_obj, interaction):
#         await interaction.response.send_message("You pressed me!")
#
#     # @discord.ui.button(label="A button", style=discord.ButtonStyle.primary,
#     #                    disabled=True)  # pass `disabled=True` to make the button pre-disabled
#     # async def button_callback(self, button_obj, interaction):
#     #     pass
#
#     @discord.ui.button(emoji="😀", label="Button 3", row=0, style=discord.ButtonStyle.primary)
#     async def button_callback(self, button_obj, interaction):
#         for child in self.children:  # loop through all the children of the view
#             child.disabled = True  # set the button to disabled
#         await interaction.response.edit_message(view=self)
#
#     @discord.ui.button(label="Button 4", row=0, style=discord.ButtonStyle.primary)
#     async def second_button_callback(self, button_obj, interaction):
#         for child in self.children:
#             child.disabled = True
#         await interaction.response.edit_message(view=self)
#
#     @discord.ui.button(label="A button", row=1, style=discord.ButtonStyle.primary)
#     async def button_callback(self, button_obj, interaction):
#         button_obj.disabled = True  # set button.disabled to True to disable the button
#         button_obj.label = "No more pressing!"  # change the button's label to something else
#         await interaction.response.edit_message(view=self)  # edit the message's view
#
#
# @bot.slash_command()  # кнопки
# async def button(ctx):
#     await ctx.respond("This is a button!", view=MyView())
# Send a message with our View class that contains the button

# class MyView(discord.ui.View):  # Вечные кнопки
#     def __init__(self):
#         super().__init__(timeout=None)  # timeout of the view must be set to None
#
#     @discord.ui.button(label="A button", custom_id="button-1", style=discord.ButtonStyle.primary, emoji="😎")
#     # the button has a custom_id set
#     async def button_callback(self, button_obj, interaction):
#         await interaction.response.send_message("Button was pressed", ephemeral=True)
#
#
# @bot.command()
# async def button(ctx):
#     await ctx.send(f"Press the button! View persistence status: {MyView.is_persistent(MyView())}", view=MyView())


@commands.is_owner()
@bot.command()
async def load(ctx, extension):
    print('--------------------------------------')
    try:
        bot.load_extension(f'cogs.{extension}')
        await ctx.respond('Ког загружен.')
    except discord.errors.ExtensionAlreadyLoaded:
        await ctx.respond('❌')
        await ctx.send('Ког уже загружен.')


@commands.is_owner()
@bot.command()
async def unload(ctx, extension):
    print('--------------------------------------')
    try:
        bot.unload_extension(f'cogsbank.{extension}')
        await ctx.respond('Ког отгружен.')
    except discord.errors.ExtensionNotLoaded:
        await ctx.message.add_reaction('❌')
        await ctx.send('Ког уже отгружен.')


@commands.is_owner()
@bot.command()
async def reload(ctx, extension):
    print('--------------------------------------')
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.respond('Ког перезагружен.')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Такой команды нет. Для просмотра списка команд, пропишите %help', delete_after=5)

    # elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    #     await ctx.send('Возможно вы пропустили какой-то аргумент. '
    #                    f'Шаблон команды - **{ctx.command.usage}**', delete_after=5)

    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send('Такого пользователя нет. Укажите ID или пинг корректно.', delete_after=5)

    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send('Произошла ошибка. повторится, обратитесь к роазработчику.', delete_after=5)
        raise error

    else:
        raise error


@bot.event
async def on_ready():
    print('------')
    print(f'Start time: {strftime("%H:%M:%S", localtime())}')
    print('Logged in as')
    print(f'Bot-Name: {bot.user.name}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(''))
    print('Status set')
    print(f'Bot-ID: {bot.user.id}')
    print(f'Discord Version: {discord.__version__}')
    bot.AppInfo = await bot.application_info()
    print(f'Owner: {bot.AppInfo.owner}')
    print('------')
    # bot.add_view(MyView())  # вечные кнопки


bot.run("Nzg1MzQ4OTAzNjY3MTA1ODMy.GGb89o.c4-FYR-qATzWdvA__WnHAsoBttOBbh6tgVS06k")
