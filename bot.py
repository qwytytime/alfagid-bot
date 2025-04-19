import telebot
from telebot import types

# Токен бота
TOKEN = '7329420392:AAGr1jaf1pPndzRBRi7eSMAXAxLotpThQFg'
bot = telebot.TeleBot(TOKEN)

# Имя Telegram-партнёра
partner_username = '@nadezdaz_kazanceva'

# Продукты по категориям
products = {
    "Дебетовые карты": {
        "Дебетовая карта": {
            "description": "Дебетовая карта с любимым кэшбэком. Бесплатное обслуживание, до 5% кэшбэка на любимые категории.",
            "link": "https://alfabank.ru/lp/retail/dc/flexible-agent/?platformId=alfapartners_msv_DC-flexible_903153_3469097"
        },
        "Детская карта": {
            "description": "Детская карта для детей от 6 до 14 лет. Бесплатная карта с кэшбэком до 5% и приложением с играми.",
            "link": "https://alfabank.ru/lp/retail/dc/childcard-agent/?platformId=alfapartners_msv_DC-childcard_903153_3469164"
        }
    },
    "Кредитные продукты": {
        "Кредитная карта 60 дней": {
            "description": "Кредитная карта с беспроцентным периодом до 60 дней и кэшбэком. Льготный период на любые покупки.",
            "link": "https://alfabank.ru/get-money/credit-cards/land/60-days-partners/?platformId=alfapartners_msv_CC-60_903153_3469224"
        },
        "Кредит наличными": {
            "description": "Кредит наличными на любые цели с суммой до 7,5 млн ₽ и ставкой от 26,5%. Онлайн-решение за 2 минуты.",
            "link": "https://alfa.me/0WwZ1h?url=https%3A%2F%2Fclick.alfabank.ru%2Fmobile-offers%2Fweb%2Fcredits%2FRP%3FisWebView%3Dtrue%26source%3Dalfapartners_msv%26referralId%3D903153&referralId=903153"
        },
        "Ипотека": {
            "description": "Ипотечный кредит на покупку недвижимости с индивидуальными условиями и возможностью подачи заявки онлайн.",
            "link": "https://alfa.me/y-6Bns?url=https%3A%2F%2Fipoteka.alfabank.ru%2Fam%3Futm_source%3Dalfapartners"
        }
    },
    "Страхование": {
        "ОСАГО": {
            "description": "Полис ОСАГО для страхования ответственности водителя перед другими участниками дорожного движения.",
            "link": "https://osago-svoy.insapp.ru/?platformId=alfapartners_msv_insurance-osago_903153_3469300"
        },
        "КАСКО": {
            "description": "Полис КАСКО для защиты от ущерба автомобилю, жизни и здоровью. Покрывает различные риски, включая угон и ДТП.",
            "link": "https://kasko-svoy.insapp.ru/?platformId=alfapartners_msv_insurance-kasko_903153_3469310"
        }
    }
}

# Главное меню
@bot.message_handler(commands=['start', 'menu'])
def send_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in products:
        markup.add(types.KeyboardButton(category))
    markup.add(types.KeyboardButton("Задать вопрос партнёру"))
    markup.add(types.KeyboardButton("Хочу стать партнёром"))
    bot.send_message(message.chat.id, "👋 Привет! Выберите категорию продукта:", reply_markup=markup)

# Меню категории
@bot.message_handler(func=lambda msg: msg.text in products.keys())
def show_category_menu(message):
    category = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for product_name in products[category]:
        markup.add(types.KeyboardButton(product_name))
    markup.add(types.KeyboardButton("🔙 Назад в главное меню"))
    markup.add(types.KeyboardButton("Задать вопрос партнёру"))
    bot.send_message(message.chat.id, f"📋 Выберите продукт из категории *{category}*:", parse_mode="Markdown", reply_markup=markup)

# Показываем информацию о продукте
@bot.message_handler(func=lambda msg: any(msg.text in product for product in products.values()))
def show_product(message):
    for category in products:
        if message.text in products[category]:
            product = products[category][message.text]
            text = f"*{message.text}*\n\n{product['description']}\n\n👉 [Оформить]({product['link']})"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("🔙 Назад в главное меню"))
            markup.add(types.KeyboardButton("Задать вопрос партнёру"))
            bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)
            break

# Обработка общих кнопок
@bot.message_handler(func=lambda msg: True)
def handle_buttons(message):
    if message.text == "🔙 Назад в главное меню":
        send_main_menu(message)
    elif message.text == "Хочу стать партнёром":
        bot.send_message(message.chat.id, f"🚀 Стать партнёром просто! Напишите нам в Telegram: {partner_username}")
    elif message.text == "Задать вопрос партнёру":
        bot.send_message(message.chat.id, f"❓ Задайте ваш вопрос партнёру: {partner_username}")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите пункт из меню.")

# Запуск бота
bot.polling(none_stop=True)
