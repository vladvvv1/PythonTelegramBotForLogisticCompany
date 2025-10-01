from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from handlers import carrier

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🚛 Перевізник", "📦 Замовник"]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Вітаю! Ви перевізник чи замовник?", reply_markup=markup)

async def role_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(text)
    if text == "🚛 Перевізник":
        await update.message.reply_text("Тут буде логіка замовника 🚀")
    elif text == "📦 Замовник":
        return await carrier.start_carrier(update, context)
        

def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, role_choice))

