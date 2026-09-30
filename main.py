import os
import random
import logging
import discord
from discord import app_commands
from dotenv import load_dotenv
from database import init_db, add_learning, get_responses, count_inputs

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/kimsw.db")
CALL_NAME = "김시원"
NO_LEARNING_MESSAGE = "# 가르치고 말이나 해"

if not TOKEN:
    raise RuntimeError("BOT_TOKEN 환경변수가 설정되지 않았습니다.")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

intents = discord.Intents.default()
intents.message_content = True

class KimSiwonBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        init_db(DATABASE_PATH)
        synced = await self.tree.sync()
        logging.info("슬래시 명령어 %d개 동기화 완료", len(synced))

bot = KimSiwonBot()

@bot.tree.command(name="가르치기", description="AI김시원에게 새로운 말을 가르칩니다.")
@app_commands.describe(
    말="김시원이 들으면 인식할 말",
    답변="그 말에 대해 김시원이 할 답변"
)
async def teach(interaction: discord.Interaction, 말: str, 답변: str):
    말 = 말.strip()
    답변 = 답변.strip()

    if not 말 or not 답변:
        await interaction.response.send_message(
            "사용법: `/가르치기 [말] [답변]`",
            ephemeral=True
        )
        return

    if len(말) > 100:
        await interaction.response.send_message(
            "말은 100자 이하로 입력해줘.",
            ephemeral=True
        )
        return

    if len(답변) > 1900:
        await interaction.response.send_message(
            "답변은 1900자 이하로 입력해줘.",
            ephemeral=True
        )
        return

    added = add_learning(DATABASE_PATH, interaction.guild_id, 말, 답변)

    if added:
        await interaction.response.send_message(
            f"'{말}'에 대한 새로운 답변을 배웠어요!"
        )
    else:
        await interaction.response.send_message(
            f"이미 배운 답변이에요! '{말}' → '{답변}'"
        )

@bot.tree.command(name="가르친횟수", description="AI김시원이 배운 서로 다른 말의 개수를 확인합니다.")
async def learned_count(interaction: discord.Interaction):
    count = count_inputs(DATABASE_PATH, interaction.guild_id)
    await interaction.response.send_message(
        f"현재 {count}개의 말을 배웠어요!"
    )

@bot.event
async def on_ready():
    logging.info("%s 로그인 완료 (ID: %s)", bot.user, bot.user.id)

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content = message.content.strip()
    prefix = CALL_NAME

    if not content.startswith(prefix):
        return

    # "김시원" 바로 뒤의 내용만 입력으로 사용
    user_input = content[len(prefix):].strip()

    if not user_input:
        return

    responses = get_responses(DATABASE_PATH, message.guild.id if message.guild else None, user_input)

    if responses:
        await message.channel.send(random.choice(responses))
    else:
        await message.channel.send(NO_LEARNING_MESSAGE)

bot.run(TOKEN)
