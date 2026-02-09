import g4f
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "8472951275:AAFDDDbYX2SW9nOhlQmmP2R9eIHtToBScVg"  # Replace with your token from @BotFather

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
ADMIN_ID = "6016855338"

# Start command
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Hello! 🤖 I am an AI assistant TYRON, created by @zufar_BRO, ask me anything")

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🔔 New user started the bot:\n"
            f"👤 Name: {message.from_user.first_name}\n"
            f"📛 Username: @{message.from_user.username if message.from_user.username else 'No username'}\n"
            f"🆔 ID: {message.from_user.id}"
        )
    )

# Echo handler (repeats your message)
@dp.message_handler()
async def echo(message: types.Message):

    quest = message.text
    response = g4f.ChatCompletion.create(
        model=("gpt-4"),
        messages=[{
            "role": "user",
            "content": quest
        }]
    )
    await message.answer(response)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
