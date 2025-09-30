from telegram.ext import ApplicationBuilder
from handlers import start, carrier, shipper, admin
from config import telegram_token

if __name__ == "__main__":
    app = ApplicationBuilder().token(telegram_token).build()

    start.register_handlers(app)
    carrier.get_carrier_handler(app)
    # shipper.register_handlers(app)
    # admin.register_handlers(app)

    print("Bot have started...")
    app.run_polling()

# from telegram import Update, ReplyKeyboardMarkup
# from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

# # Стан розмови
# CHOOSING_ROLE, CARRIER_LOCATION, CARRIER_DATE, CARRIER_VEHICLE, CARRIER_NOTES, \
# SHIPPER_CARGO, SHIPPER_PICKUP, SHIPPER_DATE, SHIPPER_NOTES = range(9)

# # Тимчасове збереження даних користувачів
# user_data = {}

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [["🚛 Перевізник", "📦 Замовник"]]
#     markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
#     await update.message.reply_text("Вітаю! Ви перевізник чи замовник?", reply_markup=markup)
#     return CHOOSING_ROLE

# async def choose_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     role = update.message.text
#     user_data[update.effective_user.id] = {"role": role}

#     # Далі обираємо тип перевезення
#     keyboard = [["🇺🇦 По Україні", "🌍 Імпорт", "📤 Експорт"]]
#     markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
#     await update.message.reply_text("Оберіть тип перевезення:", reply_markup=markup)
#     return CARRIER_LOCATION if role == "🚛 Перевізник" else SHIPPER_CARGO

# # --- Перевізник ---
# async def carrier_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     user_data[update.effective_user.id]["route_type"] = text
#     await update.message.reply_text("Де знаходиться ваше авто?")
#     return CARRIER_DATE

# async def carrier_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     user_data[update.effective_user.id]["location"] = text
#     await update.message.reply_text("Коли готові вантажитись? (дата/час)")
#     return CARRIER_VEHICLE

# async def carrier_vehicle(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     user_data[update.effective_user.id]["available_from"] = text
#     await update.message.reply_text("Вкажіть тип авто та характеристики (розміри/тоннаж)")
#     return CARRIER_NOTES

# async def carrier_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     user_data[update.effective_user.id]["vehicle_info"] = text
#     await update.message.reply_text("Додайте особливі примітки або напишіть 'Немає'")
#     return ConversationHandler.END

# # --- Замовник ---
# async def shipper_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     user_data[update.effective_user.id]["route_type"] = text
#     await update.message.reply_text("Який вантаж потрібно перевезти?")
#     return SHIPPER_PICKUP

# async def shipper_pickup(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     user_data[update.effective_user.id]["cargo_name"] = text
#     await update.message.reply_text("Звідки забрати вантаж?")
#     return SHIPPER_DATE

# async def shipper_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     user_data[update.effective_user.id]["pickup_location"] = text
#     await update.message.reply_text("Коли потрібно забрати вантаж?")
#     return SHIPPER_NOTES

# async def shipper_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     user_data[update.effective_user.id]["delivery_date"] = text
#     await update.message.reply_text("Особливі примітки? Якщо немає — напишіть 'Немає'")
#     return ConversationHandler.END

# # --- Функція відміни ---
# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("❌ Скасовано")
#     return ConversationHandler.END

# # --- Основна функція ---
# if __name__ == "__main__":
#     TOKEN = "8298873354:AAHtQ3HO8udt8Qx2h0UlzGgjoRbgPjjsl_w"
#     app = ApplicationBuilder().token(TOKEN).build()

#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler("start", start)],
#         states={
#             CHOOSING_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_role)],

#             # Перевізник
#             CARRIER_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, carrier_info)],
#             CARRIER_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, carrier_date)],
#             CARRIER_VEHICLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, carrier_vehicle)],
#             CARRIER_NOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, carrier_notes)],

#             # Замовник
#             SHIPPER_CARGO: [MessageHandler(filters.TEXT & ~filters.COMMAND, shipper_info)],
#             SHIPPER_PICKUP: [MessageHandler(filters.TEXT & ~filters.COMMAND, shipper_pickup)],
#             SHIPPER_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, shipper_date)],
#             SHIPPER_NOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, shipper_notes)],
#         },
#         fallbacks=[CommandHandler("cancel", cancel)],
#     )

#     app.add_handler(conv_handler)
#     print("Бот запущений...")
#     app.run_polling()
