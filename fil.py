from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define the bot token and channel ID
BOT_TOKEN = '7244701752:AAFKgH_nopZDQKVj1IriibSP2uWegI4e9mQ'
CHANNEL_ID = -1002209394705

# Initialize the bot
bot = Bot(token=BOT_TOKEN)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Use /filter <word> <reply> to save a reply for a word.')

def filter_command(update: Update, context: CallbackContext) -> None:
    # Extract the word and reply from the command
    args = context.args
    if len(args) < 2:
        update.message.reply_text('Usage: /filter <word> <reply>')
        return

    word = args[0]
    reply = ' '.join(args[1:])
    
    # Save the word-reply pair to the private channel
    bot.send_message(chat_id=CHANNEL_ID, text=f'{word}:{reply}')
    
    update.message.reply_text(f'Saved reply for "{word}"')

def handle_message(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    
    # Fetch the saved replies from the private channel
    updates = bot.get_updates()
    word_reply_dict = {}
    
    for update in updates:
        if update.channel_post and ':' in update.channel_post.text:
            word, reply = update.channel_post.text.split(':', 1)
            word_reply_dict[word] = reply
    
    # Check if any word in the message has a saved reply
    for word, reply in word_reply_dict.items():
        if word in message_text:
            update.message.reply_text(reply)
            break

def main() -> None:
    # Create the Updater and pass it the bot's token
    updater = Updater(token=BOT_TOKEN, use_context=True)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # Register the /start command
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Register the /filter command
    dispatcher.add_handler(CommandHandler("filter", filter_command))
    
    # Register a message handler to respond with saved replies
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
