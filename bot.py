import time
import re
from datetime import datetime
from telegram.error import NetworkError, TimedOut
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ApplicationBuilder,
    ConversationHandler,
    CommandHandler,
    filters,
    ContextTypes, 
    MessageHandler,
)
from config import save_application, send_to_broker
# from handlers import start, carrier
from config import telegram_token

ASK_TYPE, SELECT_CARRIER_OR_CUSTOMER, ASK_TYPE2, AFTER_APPLICATION, HANDLE_TYPE_OF_DELIVERY_ASK_TYPE_1, HANDLE_TYPE_OF_DELIVERY_ASK_TYPE_2 = range(6)
CUSTOMER_OR_CERRIER = 0

# 1 - carrier
# 2 - customer

QUESTIONS1 = (
    ("city", "Вкажіть місто забору (місто, вулиця, номер):"),
    ("datetime", "Введіть дату та час:"),
    ("cargo_type", "Тип вантажу:"),
    ("weight", "Вага (кг):"),
    ("capacity", "Об'єм:"),
    ("requirements", "Особливі вимоги:"),
    ("contacts", "Номер телефону: "),
    ("delivery_place", "Місце доставки: "),
)

QUESTIONS2 = (
    ("city", "Вкажіть місце забору (країна, місто, вулиця, номер):"),
    ("datetime", "Введіть дату та час:"),
    ("cargo_type", "Тип вантажу:"),
    ("weight", "Вага (кг):"),
    ("capacity", "Об'єм:"),
    ("requirements", "Особливі вимоги:"),
    ("contacts", "Номер телефону: "),
    ("delivery_place", "Місце доставки: "),
    ("customs_point", "Митний перехід: "),
    ("specific_transportation_type", "Митний термінал: "),
    ("required_documents", "Необхідні документи: "),
    ("settlements_currency", "Валюта розрахунку: "),
    ("customs_contact_person", "Контактна особа на митниці: "),
)

QUESTIONS3 = (
    ("company_name", "Вкажіть назву фірми: "),
    ("number_of_cars", "Кількість авто: "),
    ("transportation_countries", "Країни, в які здійснюються перевезення (або просто Україна): "),
    ("contacts", "Контакти: ")
)

def is_valid_number(text):
    try:
        return float(text) > 0
    except ValueError:
        return False

def is_valid_phone(text):
    return bool(re.match(r"^\+?\d{10,15}$", text))

def is_valid_datetime(text):
    try:
        datetime.strptime(text, "%d.%m.%Y %H:%M")
        return True
    except ValueError:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    print("BOT STARTED!")
    keyboard = [["Перевізник", "Замовник"]]

    await update.message.reply_text("Вітаю в програмі. Оберіть тип заявки.", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))

    return SELECT_CARRIER_OR_CUSTOMER

async def SelectCarrierOrCustomer(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    choice = update.message.text
    context.user_data["cerrier_or_customer"] = choice
    print(choice)

    if choice == "Перевізник":

        keyboard = [["По Україні", "Імпорт/Експорт"]]

        await update.message.reply_text(
                "Виберіть тип перевезення: ",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard, one_time_keyboard=True, resize_keyboard=True
                )
            )
        
        return HANDLE_TYPE_OF_DELIVERY_ASK_TYPE_1
        
    elif choice == "Замовник":

        keyboard = [["По Україні", "Імпорт/Експорт"]]

        await update.message.reply_text(
                "Виберіть тип перевезення: ",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard, one_time_keyboard=True, resize_keyboard=True
                )
            )
        
        return HANDLE_TYPE_OF_DELIVERY_ASK_TYPE_2
    else:
        await update.message.reply_text("Будь ласка, оберіть варіант із клавіатури.")
        return SELECT_CARRIER_OR_CUSTOMER
    
async def HandleTypeOfDeliveryAskTYPE1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    print("Handle ytpe of delivery ask type 1 USER_INPUT: ", user_input)

    if user_input in ("По Україні", "Імпорт/Експорт"):
        context.user_data["step"] = 0
        context.user_data["type_of_delivery"] = user_input
        print("Context user_data: ", context.user_data["type_of_delivery"])
        return await AskNext1(update, context)    
    else:
        await update.message.reply_text("Будь ласка, оберіть один із варіантів..")
        return HANDLE_TYPE_OF_DELIVERY_ASK_TYPE_1

async def HandleTypeOfDeliveryAskTYPE2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    print(user_input)
    context.user_data["type_of_delivery"] = user_input

    if user_input == "По Україні":
        context.user_data["QUESTIONS"] = QUESTIONS1
        context.user_data["step"] = 0
        return await AskNext2(update, context)
    elif user_input == "Імпорт/Експорт":
        context.user_data["QUESTIONS"] = QUESTIONS2
        context.user_data["step"] = 0
        return await AskNext2(update, context)
    else:
        await update.message.reply_text("Будь ласка, оберіть один із варіантів..")
        return HANDLE_TYPE_OF_DELIVERY_ASK_TYPE_2
   
async def AskNext1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text

    if not update.message or not update.message.text:
        await update.effective_chat.send_message("Будь ласка, введіть текст.")
        return ASK_TYPE

    current_step = context.user_data.get("step", 0)
    print(current_step)

    if current_step > 0:
        key, _ = QUESTIONS3[current_step - 1]

        if key == 'number_of_cars':
            if not is_valid_number(user_input):
                await update.message.reply_text("Будь ласка, введіть конкретне число.")
                return ASK_TYPE
        elif key == 'contacts':
            if not is_valid_phone(user_input):
                await update.message.reply_text("Будь ласка, введіть конкретний номер телефону (+380XXXXXXXXX): ")
                return ASK_TYPE

        context.user_data[key] = user_input
        print(f"{key}: {user_input}")
    
    if current_step < len(QUESTIONS3):
        key, question = QUESTIONS3[current_step]
        await update.message.reply_text(question)
        context.user_data["step"] = current_step + 1
        return ASK_TYPE
    else:
        await update.message.reply_text("Дякую, дані збережено!")
        context.user_data["step"] = 0
        print("Final data: ", context.user_data)
        
        user_id = update.effective_user.id
        type_of_delivery = context.user_data.get("type_of_delivery")
        cerrier_or_customer = context.user_data.get("cerrier_or_customer")

        if cerrier_or_customer == "Перевізник":
            app_type = "carrier"
        elif cerrier_or_customer == "Замовник":
            app_type = "international" if type_of_delivery == "Імпорт/Експорт" else "domestic"
        else:
            app_type = "unknown"

        data_to_save = {k: v for k, v in context.user_data.items() if k not in ["cerrier_or_customer", "type_of_delivery", "step"]}

        print(app_type)
            
        save_application(user_id, app_type, data_to_save)
        await send_to_broker(user_id, app_type, data_to_save)

        await after_application(update, context)
        return AFTER_APPLICATION


async def AskNext2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    

    if not update.message or not update.message.text:
        await update.effective_chat.send_message("Будь ласка, введіть текст.")
        return ASK_TYPE2
    
    QUESTIONS = context.user_data.get("QUESTIONS")
    if not QUESTIONS:
        await update.message.reply_text("Не знайдено список питань. Почніть спочатку командою /start.")
        return ConversationHandler.END
    
    current_step = context.user_data.get("step", 0)
    
    if current_step > 0:
        key, _ = QUESTIONS[current_step - 1]
        
        if key in ["weight", "capacity"]:
            if not is_valid_number(user_input):
                await update.message.reply_text("Будь ласка, введіть конкретне число.")
                return ASK_TYPE2
        elif key == "contacts":
            if not is_valid_phone(user_input):
                await update.message.reply_text("Будь ласка, введіть конкретний номер телефону (+380XXXXXXXXX)")
                return ASK_TYPE2
        elif key == "datetime":
            if not is_valid_datetime(user_input):
                await update.message.reply_text("Будь ласка, введіть дату у форматі ДД.ММ.РРРР ГГ:ХХ.")
                return ASK_TYPE2
            
        context.user_data[key] = user_input
        print(f"{key}: {user_input}")
    
    if current_step < len(QUESTIONS):
        key, question = QUESTIONS[current_step]
        await update.message.reply_text(question)
        context.user_data["step"] = current_step + 1
        return ASK_TYPE2
    else:
        await update.message.reply_text("Дякую, дані збережено!")
        context.user_data["step"] = 0
        print("Final data: ", context.user_data)

        user_id = update.effective_user.id
        type_of_delivery = context.user_data.get("type_of_delivery")
        cerrier_or_customer = context.user_data.get("cerrier_or_customer")

        if cerrier_or_customer == "Перевізник":
            app_type = "carrier"
        elif cerrier_or_customer == "Замовник":
            app_type = "international" if type_of_delivery == "Імпорт/Експорт" else "domestic"
        else:
            app_type = "unknown"

        data_to_save = {k: v for k, v in context.user_data.items() if k not in ["cerrier_or_customer", "type_of_delivery", "step", "QUESTIONS"]}

        print(app_type)
            
        save_application(user_id, app_type, data_to_save)
        await send_to_broker(user_id, app_type, data_to_save)

        await after_application(update, context)
        return AFTER_APPLICATION    

async def after_application(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [["Заповнити ще раз"], ["Завершити"]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    await update.message.reply_text(
        "Що хочеш зробити далі?", reply_markup=reply_markup
    )

    context.user_data["step"] = 0
    context.user_data["cerrier_or_customer"] = None
    context.user_data["type_of_delivery"] = None
    
    return AFTER_APPLICATION

async def handle_after_application(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    if choice == "Заповнити ще раз":
        return await start(update, context)
    elif choice == "Завершити":
        await update.message.reply_text("Дякую! До зустрічі!")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Будь ласка, оберіть одну з опцій.")
        return AFTER_APPLICATION

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and end the whole conversation"""
    await update.message.reply_text("Розмова перервана")
    context.user_data.clear()
    return ConversationHandler.END

def main():
    """run the bot."""

    application = ApplicationBuilder().token(telegram_token).build()
    print("Bot connected.")
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_CARRIER_OR_CUSTOMER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, SelectCarrierOrCustomer)
            ],
            HANDLE_TYPE_OF_DELIVERY_ASK_TYPE_2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, HandleTypeOfDeliveryAskTYPE2)
            ],
            HANDLE_TYPE_OF_DELIVERY_ASK_TYPE_1: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, HandleTypeOfDeliveryAskTYPE1)
            ],
            ASK_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, AskNext1)
            ],
            ASK_TYPE2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, AskNext2)
            ],
            AFTER_APPLICATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_after_application)
            ],  
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    while True:
        try: 
            application.run_polling(allowed_updates=Update.ALL_TYPES)
            print("Bot connected.")
        except (NetworkError, TimedOut):
            print("Network error, retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)
    
if __name__ == "__main__":
    main()


# TODO: I started only with замовник, пізніше добавлю перевізника.
# шо тобі то дає? як ти будеш звязуватися з клієнтами. що просити, шоб лишили і тд. на рахунок замовника і перевізника. перше зроблю тільки замовника. номер телефону
# перевізник. імпорт експорт україна
# потрібно де здійснює перевезення

# TODO: make a database tables
# TODO!! make the first choice normal.
# TODO: the input valid check.
# TODO: добавити після заявки вибір між ще одним написання і завершенням.

# TODO: перевірка для перевізника.

# TODO: записує type_of_devliery замість їбучого міста. треба шось придумати сука.

