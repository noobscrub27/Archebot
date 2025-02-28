import discord
from discord.ext import commands
import datetime
import enum
import logging

class BlacklistedAI(enum.Enum):
    domo_ai = 1153984868804468756
    insight_face_swap = 1090660574196674713
    viggle = 1104973139257081909
    glifbot = 1288638725869535283

class Archebot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True
        with open("token.txt", "r") as f:
            lines = f.readlines()
            self.TOKEN = str(lines[0].strip())
        super().__init__(command_prefix="!", intents=intents)
        self.run(self.TOKEN, log_level=logging.WARN)

    def timelog(self, text, return_text=False):
        now = datetime.datetime.now()
        now_text = now.strftime("%Y-%m-%d %H:%M:%S")
        text = f"[{now_text}] - {text}"
        print(text)
        if return_text:
            return text

    async def on_ready(self):
        self.timelog(f"Logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.author.id in [ai_id.value for ai_id in BlacklistedAI]:
            await message.delete()
            self.timelog("Deleted an AI message.")

bot = Archebot()
