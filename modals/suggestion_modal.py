import discord

from discord import ui
from utils.database import SuggestionDatabase

class SuggestionsModal(ui.Modal, title = 'Suggest a new response for us!'):

    bot_input = ui.TextInput(label = 'Inputs', style = discord.TextStyle.long, required = True, placeholder = 'List your inputs.')
    responses = ui.TextInput(label = 'Responses', style = discord.TextStyle.long, required = True, placeholder = 'List your responses for an input.')
    notes = ui.TextInput(label = 'Notes', style = discord.TextStyle.long, required = False, placeholder = 'Write some details about your suggeston.')

    def __init__(self, db: SuggestionDatabase):
        super().__init__()
        self.__db = db


    async def on_submit(self, interaction: discord.Interaction):

        user = interaction.user.name

        self.__db.add_suggestion('dl_suggestions', user, self.bot_input.value, self.responses.value, self.notes.value)        
        await interaction.response.send_message('Thank you for suggestion!')