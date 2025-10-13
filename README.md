<<<<<<< HEAD
# PythonTelegramBotForLogisticCompany
=======
Logistic Helper

logistics_bot/
│
├── bot.py                  # Основний файл запуску бота
├── config.py               # Конфігурації: TOKEN, база даних, налаштування
├── requirements.txt        # Бібліотеки для проекту
│
├── handlers/               # Обробники команд і повідомлень
│   ├── __init__.py
│   ├── start.py            # /start та вибір ролі користувача
│   ├── carrier.py          # Обробка перевізників
│   ├── shipper.py          # Обробка замовників
│   ├── admin.py            # Обробники для адміна
│
├── keyboards/              # Клавіатури та кнопки
│   ├── __init__.py
│   ├── main.py             # Основне меню
│   ├── role_selection.py   # Кнопки перевізник/замовник
│
├── models/                 # Схеми для бази даних
│   ├── __init__.py
│   ├── user.py
│   ├── carrier_request.py
│   ├── shipper_request.py
│   ├── match.py
│
├── database/               # Модуль роботи з БД
│   ├── __init__.py
│   ├── connection.py       # Підключення до SQLite/MySQL/PostgreSQL
│   ├── crud.py             # Створення, читання, оновлення, видалення записів
│
├── utils/                  # Утиліти та допоміжні функції
│   ├── __init__.py
│   ├── validators.py       # Перевірка дати, формату, адреси
│   ├── notifications.py    # Надсилання повідомлень адміну або групі
│
└── logs/                   # Логи бота
    └── bot.log


-- Ролі у системі --
1.1 Carrier (Transporter)
- Domestic (within Ukraine)
Vehicle operates only inside the country.
- Import / Export (International)
Vehicle can handle shipments across the border.
May require international licenses and customs documentation.

1.2 Customer (Shipper)
- Domestic (within Ukraine)
Requests shipment within the country.
- Import / Export (International)
Requests shipment across the border.
Requires customs paperwork, certifications, and special country-specific regulations.

Submission process with Categories
2.1 Carrier Submission
1. Carrier selects shipment type (Domestic or Import/Export)
2. Bot asks for:
- Vehicle location
- Availability (data/time)
- Vahicle type, dimensions, capacity
- Special characteristics (refrigerated, open beb, covered, etc.)
- For import/export: documentation for international transport.
3. Data stored in the database along with the shipment category.

2.2 Customer Submission
1. Customer selects shipment type (Domestic or Import / Export)
2. Bot asks for:
- Pickup location
- Pickup date and time
- Cargo type, weight, volume
- Special instructions (fragile, hazardous, perishable, temperature requirements)
- For import/export: customs documents, origin/destination country
3. Data is stored in the database with the shipment category.

3. Matching Logic with Categories
1. Bot compares shipment categories of carriers and customers:
- Domestic → only match domestic carriers with domestic shipments.
- Import / Export → only match international carriers with international shipments, verifying documentation.
2. Additional matching criteria:
- Vehicle location vs. cargo pickup location
- Vehicle availability vs. cargo pickup time
- Vehicle features vs. cargo requirements

1. Основна логіка

Замовник:

Створює заявку на перевезення вантажу.

Вказує всі параметри вантажу: місце забору, дату/час, тип вантажу, об’єм/вагу, особливі вимоги, категорію перевезення (по Україні або міжнародне).

Його мета — знайти перевізника, який підходить під ці вимоги.

Перевізник:

Має список доступних вантажів (заявок від замовників), які бот йому пропонує на основі параметрів авто та категорії перевезення.

Перевіряє вантажі, вибирає ті, які може забрати.

“Бере замовлення” — бот оновлює статус заявки, і замовник бачить, що перевізник узгодив перевезення.

Перевізник → що він може доставити, коли і де його авто доступне, характеристики авто, документи (для міжнародних перевезень).

Замовник → що потрібно перевезти, куди, коли, особливі вимоги, документи (для міжнародних перевезень).


Так, ти майже правильно описав, але є кілька уточнень, щоб процес був логічно точний:

---

## **Сценарій роботи бота**

### **1. Замовник заходить у бота**

1. Відкриває бота → обирає: **“Я замовник”**
2. Обирає категорію перевезення: **“По Україні”** або **“Імпорт / Експорт”**
3. Вводить дані про вантаж:

   * Місце забору
   * Дату та час, коли вантаж потрібно забрати
   * Тип вантажу, вага, об’єм
   * Особливі вимоги (температура, крихкий, небезпечний тощо)
4. Вводить, якщо потрібно, додаткові параметри (наприклад, чи вантаж потребує спеціального авто).

---

### **2. Збереження заявки**

* Бот зберігає усі дані у базі.
* Замовник отримує підтвердження: “Ваша заявка прийнята. Чекайте, поки перевізник візьме її у роботу.”

---

### **3. Далі вступає перевізник**

1. Перевізник заходить у бота → обирає: **“Я перевізник”**
2. Бот показує список доступних вантажів, відфільтрованих за параметрами його авто та категорією перевезення.
3. Перевізник вибирає вантаж → підтверджує, що він його забере.

---

### **4. Підтвердження замовнику**

* Замовник отримує повідомлення:
  “Ваш вантаж буде перевезено перевізником [Ім’я], авто [тип/розміри], дата забору [дата/час].”
* Статус заявки оновлюється на “Вантаж взято у перевезення”.

---

💡 **Підсумок:**

1. Замовник → створює заявку і чекає.
2. Перевізник → бачить заявки → обирає, що може забрати.
3. Бот → зв’язує замовника і перевізника, оновлює статус.

---

Якщо хочеш, я можу зробити **графічну блок-схему цього процесу** з усіма кроками для замовника та перевізника. Це буде наочно і дуже допоможе для розробки бота.

Хочеш, щоб я її зробив?
>>>>>>> 68ce251 (Carrier.py working on)
