from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import time

TOKEN = '7322708595:AAExdf_Swh65yIOvHHbBRXrJXGJb15N1mSY'
DEVELOPER_CONTACT = 'Ruined_soul'

# Track the bot's start time
start_time = time.time()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type == 'private':
        keyboard = [
            [InlineKeyboardButton("Add me to your group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
            [InlineKeyboardButton("Contact Developer", url=f"https://t.me/{DEVELOPER_CONTACT}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Welcome! Use /all to tag all users and /admin to tag all admins.', reply_markup=reply_markup)
    else:
        await update.message.reply_text("Thanks for adding me! I am ready to nag them all.")

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
    # Calculate uptime
    uptime_seconds = int(time.time() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"
    
    # Here you would calculate the speed and ping, but it depends on what metrics you want.
    # For simplicity, we'll just report the uptime.
    
    await update.message.reply_text(f"Bot is alive! Uptime: {uptime_str}")

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("all", all_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("alive", alive_command))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
