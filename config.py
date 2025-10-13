from dotenv import load_dotenv
import os
from supabase import create_client, Client
from telegram import Bot

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
broker_telegram_token = os.getenv("BROKER_TELEGRAM_TOKEN")
BROKER_CHAT_ID = int(os.getenv("BROKER_CHAT_ID", "0"))

if not all([supabase_url, supabase_key, broker_telegram_token, BROKER_CHAT_ID]):
    raise ValueError("❌ Missing environment variables in .env")

supabase: Client = create_client(supabase_url, supabase_key)
broker_bot = Bot(token=broker_telegram_token)


def save_application(user_id: int, app_type: str, data: dict):
    """Зберігає заявку у таблицю applications."""
    return supabase.table("applications").insert({
        "user_id": user_id,
        "application_type": app_type,
        **data
    }).execute()


async def send_to_broker(user_id: int, app_type: str, data: dict):
    titles = {
        "domestic": "🚛 Заявка по Україні",
        "international": "🌍 Імпорт/Експорт",
        "carrier": "🚚 Перевізник",
    }
    title = titles.get(app_type, "📨 Нова заявка")

    # Прибираємо технічні ключі
    keys_to_skip = ["step", "cerrier_or_customer", "type_of_delivery"]
    clean_data = {k: v for k, v in data.items() if k not in keys_to_skip}

    # Українські підписи
    labels_uk = {
        "city": "Місто забору",
        "datetime": "Дата та час",
        "cargo_type": "Тип вантажу",
        "weight": "Вага (кг)",
        "capacity": "Об'єм",
        "requirements": "Особливі вимоги",
        "contacts": "Контакти",
        "delivery_place": "Місце доставки",
        "customs_point": "Митний пункт",
        "specific_transportation_type": "Тип транспортування",
        "required_documents": "Необхідні документи",
        "settlements_currency": "Валюта розрахунку",
        "customs_contact_person": "Контактна особа на митниці",
        "company_name": "Назва компанії",
        "number_of_cars": "Кількість авто",
        "transportation_countries": "Країни перевезення"
    }

    # Формуємо текст
    text_lines = []
    for k, v in clean_data.items():
        label = labels_uk.get(k, k)
        text_lines.append(f"<b>{label}</b>: {v}")

    text = f"<b>{title}</b>\n\n" + "\n".join(text_lines)

    # Надсилаємо брокеру
    try:
        await broker_bot.send_message(chat_id=BROKER_CHAT_ID, text=text, parse_mode="HTML")
    except Exception as e:
        print(f"⚠️ Помилка при надсиланні брокеру: {e}")
