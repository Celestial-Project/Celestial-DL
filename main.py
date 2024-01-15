import os
import discord
import argparse

from dotenv import load_dotenv
from discord.ext import commands

import utils.database
from utils.loader import load_chat_model
from utils.chat_processing import process_message
from utils.logger import info_log, error_log, clear_log
from utils.modals.suggestion_modal import SuggestionsModal

flags_parser = argparse.ArgumentParser(
    prog = 'Celestial Discord Bot',
    description = 'A discord bot integrated with Celestial chat model',
)

flags_parser.add_argument('-d', '--debug', action='store_true')
flags_parser.add_argument('-m', '--model', type=str)

use_debug_mode = flags_parser.parse_args().debug
selected_model = flags_parser.parse_args().model

load_dotenv()

(model, model_name, data, label_encoder, word_encoder) = load_chat_model() if not selected_model else load_chat_model(selected_model)

db_connection = utils.database.create_database_connection(os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_PASS'))
suggestion_db = utils.database.SuggestionDatabase(db_connection)

intents = discord.Intents.default()
intents.message_content = True

bot_channel_name = 'celestial-chat'

client = commands.Bot(
    command_prefix = '::$', 
    intents = intents, 
    help_command = None,
    activity = discord.Game(name = '`/help` for more info.')
)

@client.event
async def on_ready() -> None:
    
    if not use_debug_mode:
        clear_log()

    info_log('Syncing slash commands...')
    
    try:
        synced = await client.tree.sync()
        
    except Exception as e:
        error_log(f'Exception detected: \n{e}')

    if not use_debug_mode:
        clear_log()

    info_log(f'Synced: {len(synced)} commands' if len(synced) != 1 else f'Synced: {len(synced)} command')
    info_log(f'Status: {"Debug" if use_debug_mode else "Production"}')
    info_log(f'Model name: {model_name}')
    info_log(f'Successfully logged in as: {client.user}')


@client.event
async def on_message(message: discord.Message) -> None:
    
    if (message.channel.name != bot_channel_name) or (message.author == client.user):
        return
    
    chat_message = message.content.strip()
    await message.channel.send(process_message(chat_message, model, data, label_encoder, word_encoder, debug = use_debug_mode))
    
    
@client.event
async def on_command_error(_ctx: commands.context.Context, error: any):
    
    if isinstance(error, discord.errors.PrivilegedIntentsRequired):
        error_log('Error: Privileged Intents Gateway is not enabled. Please enable it first at: https://discord.com/developers')
        
    elif isinstance(error, discord.errors):
        pass
    
    
@client.tree.command(name = 'setup-chat', description = 'Setup a text channel for Celestial chat.')
async def setup_chat(interaction: discord.Interaction) -> None:
    
    guild = interaction.guild
    channel_list = [ch.name for ch in guild.text_channels]
    
    if bot_channel_name in channel_list:
        await interaction.response.send_message(f'<#{discord.utils.get(guild.text_channels, name = bot_channel_name).id}> is already existed.')
        return
    
    await guild.create_text_channel(bot_channel_name)
    await interaction.response.send_message('Setup complete!')


@client.tree.command(name = 'suggestion', description = 'Suggest a new intents for next version.')
async def suggestion(interaction: discord.Interaction) -> None:
    await interaction.response.send_modal(SuggestionsModal(suggestion_db))

    
@client.tree.command(name = 'help', description = 'Display a help message.')
async def helper(interaction: discord.Interaction) -> None:
    
    help_embed = discord.Embed(
        title = '', 
        description = 'a deep-learning Python Discord chatbot who can talk with you in English and Thai.', 
        color = 0xd357fe
    )
    
    help_embed.set_author(
        name = 'Celestial-DL#8254', 
        icon_url = client.user.avatar._url
    )
    
    help_embed.add_field(
        name = 'How can you talk with me?', 
        value = 'Use `/setup-chat` to setup text channel for me first and then you could just send me a message now.', 
        inline = False
    )
    
    help_embed.add_field(
        name = 'Wanna teach me something?', 
        value = 'Use `/suggestion` to suggest new response for me!', 
        inline = False
    )
    
    help_embed.add_field(
        name = 'Report Issue', 
        value = 'If there is a problem with the bot response or any bug with me, \nfeel free to report it to our creator at: **[Github issues](https://github.com/Celestial-Project/Celestial-DL/issues)**', 
        inline = True
    )
    
    help_embed.add_field(
        name = 'Development & Update', 
        value = 'Follow the latest update at: **[Github repository](https://github.com/Celestial-Project/Celestial-DL)**', 
        inline = False
    )
    
    help_embed.set_footer(text = '© 2023 MIT License - @strixziv')
    
    await interaction.response.send_message(embed = help_embed)


if __name__ == '__main__':
    process_message('hello', model, data, label_encoder, word_encoder)
    client.run(os.getenv('TOKEN'))