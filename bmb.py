from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = 'YOUR_BOT_TOKEN'
DEVELOPER_CONTACT = 'YOUR_CONTACT_USERNAME'

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Add me to your group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("Contact Developer", url=f"https://t.me/{DEVELOPER_CONTACT}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome! Use /all to tag all users and /admin to tag all admins.', reply_markup=reply_markup)

def all_command(update: Update, context: CallbackContext) -> None:
    chat = update.message.chat
    members = chat.get_members()
    tags = [f'@{member.user.username}' for member in members if member.user.username]
    if tags:
        update.message.reply_text(' '.join(tags))
    else:
        update.message.reply_text("No users to tag.")

def admin_command(update: Update, context: CallbackContext) -> None:
    chat = update.message.chat
    admins = chat.get_administrators()
    tags = [f'@{admin.user.username}' for admin in admins if admin.user.username]
    if tags:
        update.message.reply_text(' '.join(tags))
    else:
        update.message.reply_text("No admins to tag.")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("all", all_command))
    dispatcher.add_handler(CommandHandler("admin", admin_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
