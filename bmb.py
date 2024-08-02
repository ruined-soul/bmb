from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import time

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '7322708595:AAExdf_Swh65yIOvHHbBRXrJXGJb15N1mSY'
DEVELOPER_CONTACT = 'Ruined_soul'

start_time = time.time()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Add me to your group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("Contact Developer", url=f"https://t.me/{DEVELOPER_CONTACT}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome! Use /all to tag all users and /admin to tag all admins.', reply_markup=reply_markup)

async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.message.chat
    members = await chat.get_members()
    tags = [f'@{member.user.username}' for member in members if member.user.username]
    if tags:
        await update.message.reply_text(' '.join(tags))
    else:
        await update.message.reply_text("No users to tag.")

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.message.chat
    admins = await chat.get_administrators()
    tags = [f'@{admin.user.username}' for admin in admins if admin.user.username]
    if tags:
        await update.message.reply_text(' '.join(tags))
    else:
        await update.message.reply_text("No admins to tag.")

async def alive_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current_time = time.time()
    uptime = current_time - start_time
    # Calculate speed (dummy value for illustration)
    speed = "N/A"
    # Calculate ping (dummy value for illustration)
    ping = "N/A"
    
    response = (f"Bot is alive!\n"
                f"Uptime: {uptime:.2f} seconds\n"
                f"Speed: {speed}\n"
                f"Ping: {ping}")
    await update.message.reply_text(response)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if chat_id > 0:  # If it's a private chat
        response = ("/start - Start the bot\n"
                    "/all - Tag all users\n"
                    "/admin - Tag all admins\n"
                    "/alive - Check bot status and uptime")
        await update.message.reply_text(response)
    else:  # If it's a group chat
        keyboard = [
            [InlineKeyboardButton("Get help in PM", url=f"https://t.me/{context.bot.username}?start=help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("To get help, please check your private messages.", reply_markup=reply_markup)

async def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("all", all_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("alive", alive_command))
    application.add_handler(CommandHandler("help", help_command))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
