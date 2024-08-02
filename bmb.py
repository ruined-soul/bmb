from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.helpers import escape_markdown

TOKEN = '7322708595:AAExdf_Swh65yIOvHHbBRXrJXGJb15N1mSY'
DEVELOPER_CONTACT = 'Ruined_soul'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Add me to your group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("Contact Developer", url=f"https://t.me/{DEVELOPER_CONTACT}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome! Use /all to tag all users and /admin to tag all admins.', reply_markup=reply_markup)

async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.message.chat
    members = await chat.get_members()  # Note: This line assumes you have a method to get members, which might not exist.
    tags = [f'@{member.user.username}' for member in members if member.user.username]
    if tags:
        await update.message.reply_text(' '.join(tags))
    else:
        await update.message.reply_text("No users to tag.")

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.message.chat
    admins = await chat.get_administrators()  # Note: This line assumes you have a method to get admins.
    tags = [f'@{admin.user.username}' for admin in admins if admin.user.username]
    if tags:
        await update.message.reply_text(' '.join(tags))
    else:
        await update.message.reply_text("No admins to tag.")

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("all", all_command))
    application.add_handler(CommandHandler("admin", admin_command))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
