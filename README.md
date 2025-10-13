# 📋 Documentation: Telegram Bot "Logistics Application System"

## 🎯 Overview
A Telegram bot for collecting logistics applications from carriers and customers with delivery type classification.

## 🔗 Basic Commands
- `/start` - Start conversation, clear previous data
- `/cancel` - Cancel conversation, clear all data

## 🏗 Bot Architecture

### Conversation States
```python
ASK_TYPE, SELECT_CARRIER_OR_CUSTOMER, ASK_TYPE2, AFTER_APPLICATION, 
HANDLE_TYPE_OF_DELIVERY_ASK_TYPE_1, HANDLE_TYPE_OF_DELIVERY_ASK_TYPE_2, 
EDITED_MESSAGE_HANDLER = range(7)
```

### User Flow
```
/start → Select Role → Select Delivery Type → Answer Questions → Submit → Repeat/Finish
```

## 👥 User Roles & Question Sets

### 1. **Carrier** (`Перевізник`)
- **Question Set**: QUESTIONS3
- **Purpose**: Company registration for service providers
- **Questions**:
  - Company name
  - Number of vehicles
  - Operating countries
  - Contact information

### 2. **Customer** (`Замовник`)
Two delivery types with different question sets:

#### **Domestic** (`По Україні`)
- **Question Set**: QUESTIONS1
- **Questions**: City, datetime, cargo type, weight, capacity, requirements, contacts, delivery place

#### **International** (`Імпорт/Експорт`)
- **Question Set**: QUESTIONS2  
- **Additional Questions**: Customs point, terminal, documents, currency, customs contact

## 📊 Data Validation

### Validation Functions
- `is_valid_number()` - Positive numbers for weight/capacity
- `is_valid_phone()` - Phone number format (+XXXXXXXXXXX)
- `is_valid_datetime()` - Date format (DD.MM.YYYY HH:MM)

### Navigation
- **Back button** (`⏪ Назад`) - Step-by-step backward navigation
- **Edit restriction** - Message editing is blocked with warning

## 💾 Data Processing

### Storage Functions
- `save_application(user_id, app_type, data)` - Save to database
- `send_to_broker(user_id, app_type, data)` - Send to message broker

### Application Types
```python
# Carrier
app_type = "carrier"

# Customer  
app_type = "international"  # Імпорт/Експорт
app_type = "domestic"       # По Україні
```

## 🛡 Error Handling

### Global Error Handler
- Catches all unhandled exceptions
- User-friendly error messages
- Detailed logging with traceback

### Network Resilience
- Automatic retry on network errors
- 5-second delay between retries
- Continuous polling with error recovery

## 🔄 Post-Submission Flow

### After Application Options
- **Fill again** (`Заповнити ще раз`) - Restart conversation
- **Finish** (`Завершити`) - End conversation

### Data Cleanup
- User data cleared after completion
- Step counters reset
- Role and delivery type reset

## 🚀 Deployment

### Requirements
- Python 3.7+
- python-telegram-bot library
- Telegram Bot Token

### Key Features
- ✅ Persistent conversation states
- ✅ Data validation
- ✅ Error recovery
- ✅ User-friendly navigation
- ✅ Multi-language support (Ukrainian)
- ✅ Network resilience

## 📝 Usage Example

```
User: /start
Bot: Welcome! Choose application type [Carrier/Customer]

User: Customer  
Bot: Choose delivery type [Domestic/International]

User: International
Bot: [Question 1]: Specify pickup location...
[Continues through all questions]

Bot: Thank you! Data saved. [Repeat/Finish options]
```

## 🔧 Configuration
- Token stored in `telegram_token`
- Modular handler structure
- Easy to extend with new question sets