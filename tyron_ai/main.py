import re
import g4f
import pandas as pd
from aiogram import Bot, Dispatcher, executor, types
from pathlib import Path
from datetime import datetime
import config

API_TOKEN = config.BOTTOKEN
ADMIN_ID = config.admin_id

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

FORBIDDEN_NAMES = ["chatgpt", "gpt", "claude", "bard", "gemini", "llama", "mistral"]

DB_FILE = Path("users.xlsx")

if not DB_FILE.exists():
    df = pd.DataFrame(columns=["UserID", "Name", "Username", "First Seen"])
    df.to_excel(DB_FILE, index=False)

def add_user_to_db(user_id, name, username):
    df = pd.read_excel(DB_FILE)

    if user_id not in df["UserID"].values:
        new_row = {
            "UserID": user_id,
            "Name": name,
            "Username": username or "No username",
            "First Seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(DB_FILE, index=False)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    name = message.from_user.first_name
    username = message.from_user.username
    user_id = message.from_user.id

    add_user_to_db(user_id, name, username)

    await message.reply(f"Hello {message.from_user.first_name}!\n"
                        "🤖 I am an AI assistant TYRON, created by @zufar_BRO, ask me anything\n"
                        "Send your questions in 1 Text, Multiple texts is considered in different chats!")

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🔔 New user started the bot:\n"
            f"👤 Name: {name}\n"
            f"📛 Username: @{username or 'No username'}\n"
            f"🆔 ID: {user_id}"
        )
    )

@dp.message_handler()
async def echo(message: types.Message):
    quest = message.text.strip().lower()

    if re.search(r'\b(?:' + '|'.join(FORBIDDEN_NAMES) + r')\b', quest):
        await message.answer("⚠️ You are calling me by forbidden names. I am Tyrone AI 🤖")
        return

    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        raw_response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}]
        )

        response = (
            raw_response.get("choices", [{}])[0]
            .get("message", {})
            .get("content", str(raw_response))
            if isinstance(raw_response, dict)
            else str(raw_response)
        )

    except Exception as e:
        response = f"⚠️ Error generating response: {e}"

    for i in range(0, len(response), 4000):
        await message.answer(response[i:i + 4000])

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
