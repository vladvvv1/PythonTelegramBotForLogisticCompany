from telegram import Update, ReplyKeyboardMarkup
from telegram.next import CommandHandler, ContextTypes

def register_handlers(app):
    add.add_handler(CommandHandler("start", start))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🚛 Перевізник", "📦 Замовник"]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Вітаю! Ви перевізник чи замовник?", reply_markup=markup)