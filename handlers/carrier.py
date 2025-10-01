from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler, 
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

ASK_TYPE, ASK_INTERNAL_CITY, ASK_INTERNAL_DATE, ASK_IMPORT_MODE = range(4)

async def start_carrier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔹 Команда /carrier отримана")
    keyboard = [["Внутрішні перевезення", "Імпорт/Експорт"]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Виберіть тип перевезення: ", reply_markup=markup)
    return ASK_TYPE

async def handle_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    print(f"🔹 Користувач обрав: {choice}")
    context.user_data["type"] = choice

    if choice == "Внутрішні перевезення":
        print("🔹 Перехід до ASK_INTERNAL_CITY")
        await update.message.reply_text("Вкажіть місто забору: ")
        return ASK_INTERNAL_CITY
    
    elif choice == "Імпорт/Експорт":
        print("🔹 Перехід до ASK_IMPORT_MODE")
        await update.message.reply_text("Вкажіть країну призначення: ")
        return ASK_IMPORT_MODE
    else:
        await update.message.reply_text("Невірний вибір. Спробуйте ще раз.")
        return ASK_TYPE

async def handle_internal_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    print(f"🔹 Місто отримано: {city}")
    context.user_data["city"] = city
    await update.message.reply_text("Вкажіть дату відправлення: ")
    return ASK_INTERNAL_DATE

async def handle_internal_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date = update.message.text
    print(f"🔹 Дата отримана: {date}")
    context.user_data["date"] = date
    
    summary = (
        f"✅ Дані збережені!\n"
        f"Тип: {context.user_data['type']}\n"
        f"Місто: {context.user_data['city']}\n"
        f"Дата: {context.user_data['date']}"
    )
    await update.message.reply_text(summary)
    print("🔹 Конверсація завершена")
    return ConversationHandler.END

async def handle_import_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = update.message.text
    print(f"🔹 Країна отримана: {mode}")
    context.user_data["mode"] = mode
    
    summary = f"✅ Дані збережені!\nТип: {context.user_data['type']}\nКраїна: {mode}"
    await update.message.reply_text(summary)
    print("🔹 Конверсація завершена")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Розмова перервана")
    context.user_data.clear()
    return ConversationHandler.END

def get_carrier_handler():
    print("🔹 Carrier handler створено")
    return ConversationHandler(
        entry_points=[CommandHandler("carrier", start_carrier)],
        states={
            ASK_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_type)
            ],
            ASK_INTERNAL_CITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_internal_city)
            ],
            ASK_INTERNAL_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_internal_date)
            ],
            ASK_IMPORT_MODE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_import_mode)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )