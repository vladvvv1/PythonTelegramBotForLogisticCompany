import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ApplicationBuilder,
    ConversationHandler,
    CommandHandler,
    filters,
    ContextTypes, 
    MessageHandler,
)
from handlers import start, carrier
from config import telegram_token

TYPE_OF_DELIVERING, ASK_TYPE = range(2)

QUESTIONS = (
    ("city", "Вкажіть місто забору (місто, вулиця, номер):"),
    ("datetime", "Введіть дату та час:"),
    ("cargo_type", "Тип вантажу:"),
    ("weight", "Вага (кг):"),
    ("capacity", "Об'єм:"),
    ("requirements", "Особливі вимоги:"),
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("BOT STARTED!")
    """Start the conversation and give the question."""
    keyboard = [["По Україні", "Імпорт/Експорт"]]

    await update.message.reply_text(
        "Вітаю в програмі. Виберіть тип перевезення: ", reply_markup=ReplyKeyboardMarkup(
            keyboard, one_time_keyboard=True, resize_keyboard=True,
        ),
    )
    
    return TYPE_OF_DELIVERING

async def TypeOfDelivering(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    context.user_data["delivery_type"] = choice
    print("Delivery type: ", choice)

    if choice == "По Україні":
        key, question = QUESTIONS[0]
        await update.message.reply_text(question)
        context.user_data["step"] = 1
        return ASK_TYPE
    elif choice == "Імпорт/Експорт":
        await update.message.reply_text("Вкажіть країну забору (країна, місто, вулиця, номер): ")
        return ASK_EXPORTORIMPORT_CITY
    else:
        await update.message.reply_text("Будь ласка, оберіть варіант із клавіатури.")
        return TYPE_OF_DELIVERING

async def ask_next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    
    # store the last user answer
    current_step = context.user_data.get("step", 1)
    if current_step > 0:
        key, _ = QUESTIONS[current_step - 1]
        context.user_data[key] = user_input
        print(f"{key}: {user_input}")
    
    if current_step < len(QUESTIONS):
        key, question = QUESTIONS[current_step]
        await update.message.reply_text(question)
        context.user_data["step"] = current_step + 1
        return ASK_TYPE
    else:
        # end of the dialog
        await update.message.reply_text("Дякую, дані збережено!")
        print("Final data: ", context.user_data)
        return ConversationHandler.END

# async def AskInternalCity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     country = update.message.text
#     print("City: ", country)
    
#     await update.message.reply_text("Введіть дату та час: ")

#     return ASK_DATE_TIME

# async def AskDateTime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     dateTime = update.message.text
#     print("Date time: ", dateTime)

#     await update.message.reply_text("Тип вантажу: ")
#     return ASK_CARGO_TYPE

# async def AskCargoType(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     cargoType = update.message.text
#     print("Cargo type: ", cargoType)

#     await update.message.reply_text("Вага (кг): ")
#     return ASK_WEIGHT

# async def AskWeight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     weight = update.message.text
#     print("Weight: ", weight)

#     await update.message.reply_text("Об'єм: ")
#     return SPECIAL_REQUIREMENTS

# async def AskCapacity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     capacity = update.message.text
#     print("Capacity: ", capacity)

#     await update.message.reply_text("Особливі вимоги: ")
#     return ASK_SPECIAL_REQUIREMENTS 

# async def AskSpecialRequirements(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     requirements = update.message.text
#     print("Requirements: ", requirements)

#     await update.message.reply_text(": ")
#     return SPECIAL_REQUIREMENTS

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and end the whole conversation"""
    await update.message.reply_text("Розмова перервана")
    context.user_data.clear()
    return ConversationHandler.END

def main():
    """run the bot."""

    application = ApplicationBuilder().token(telegram_token).build()
    print(TYPE_OF_DELIVERING)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TYPE_OF_DELIVERING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, TypeOfDelivering)
            ],
            ASK_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_next)
            ]
            # ASK_DATE_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, AskDateTime)],
            # ASK_CARGO_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, AskCargoType)],
            # ASK_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, AskWeight)],
            # ASK_CAPACITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, AskCapacity)]
            # ASK_SPECIAL_REQUIREMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, AskSpecialRequirements)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()


# TODO: I started only with замовник, пізніше добавлю перевізника.