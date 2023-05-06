import os
import discord
import argparse

from dotenv import load_dotenv
from discord.ext import commands
from chat_processing import process_message

from utils.loader import get_model_version
from utils.logger import info_log, error_log

flags_parser = argparse.ArgumentParser()
flags_parser.add_argument('-d', '--debug', action='store_true')

use_debug_mode = flags_parser.parse_args().debug

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(
    command_prefix = '::</!' if use_debug_mode else '</!', 
    intents = intents, 
    help_command = None,
    activity = discord.Game(name = '/help for more info.')
)

@client.event
async def on_ready() -> None:

    os.system('cls' if os.name == 'nt' else 'clear')

    info_log('Syncing slash commands...')
    
    try:
        synced = await client.tree.sync()
        
    except Exception as e:
        error_log(f'Exception detected: \n{e}')

    os.system('cls' if os.name == 'nt' else 'clear')

    info_log(f'Synced: {len(synced)} commands' if len(synced) != 1 else f'Synced: {len(synced)} command')
    info_log(f'Status: {"Debug" if use_debug_mode else "Production"}')
    info_log(f'Model version: {get_model_version("./model")}')
    info_log(f'Successfully logged in as: {client.user}')


@client.event
async def on_message(message: discord.Message) -> None:

    if message.content.startswith('</usr>'):
        
        chat_message = message.content.split('</usr>')[1].strip()
        
        if not chat_message or chat_message == '':
            await message.delete()
            return
        
        await message.channel.send(process_message(chat_message, debug = use_debug_mode))

    await client.process_commands(message)
    
    
@client.tree.command(name = 'setup-chat', description = 'Setup a text channel for Celestial chat.')
async def setup_chat(interaction: discord.Interaction) -> None:
    
    guild = interaction.guild
    
    channel_list = [ch.name for ch in guild.text_channels]
    
    if 'celestial-chat' in channel_list:
        await interaction.response.send_message('Celestial text channel is already existed.')
        return
    
    await guild.create_text_channel('celestial-chat')
    await interaction.response.send_message('Setup complete!')

    
@client.tree.command(name = 'help', description = 'Display a help message.')
async def helper(interaction: discord.Interaction) -> None:
    
    help_embed = discord.Embed(
        title = '', 
        description = 'an experimental deep-learning Python Discord chat bot who can talk with you in English and Thai.', 
        color = 0xd357fe
    )
    
    help_embed.set_author(
        name = 'Celestial-DL#8254', 
        icon_url = 'https://cdn.discordapp.com/app-icons/927573556961869825/b4b624c1cb68fa3a99a24a8e9942d2a5.png'
    )
    
    help_embed.add_field(
        name = 'How can you talk to me?', 
        value = 'You can talk to me by simply type\n`</usr> Your messages` to send me a messages!', 
        inline = False
    )
    
    help_embed.add_field(
        name = 'Report Issue', 
        value = 'If there is a problem with the bot response or any bug with the bot, \nfeel free to report us at: \n**https://github.com/StrixzIV/Celestial-DL/issues**', 
        inline = True
    )
    
    help_embed.add_field(
        name = 'Development & Update', 
        value = 'Follow the latest update at: \n**https://github.com/StrixzIV/Celestial-DL**', 
        inline = False
    )
    
    help_embed.set_footer(text = '© 2023 MIT License - StrixzIV#6258')
    
    await interaction.response.send_message(embed = help_embed)


if __name__ == '__main__':

    process_message('a')
    load_dotenv()
    
    client.run(os.getenv('TOKEN'))