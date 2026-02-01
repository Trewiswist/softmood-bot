import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 1612110248  # твой Telegram ID

# ---- КАТЕГОРИИ И ТОВАРЫ ----
CATEGORIES = {
    "dresses": {
        "title": "👗 Платья",
        "items": [
            {
    "name": "Платье из двухсторонней ангоры с вышивкой ✨ 7560",
    "price": "1165 ₴",
    "description": "Мягчайшая двухсторонняя ангора 🤍\nВысокий уютный гольф + роскошная вышивка на рукавах 🌿\n\nСвободный крой — полная свобода движений 💫\nДлина миди\nОбъёмные рукава с манжетами\n\nЦвета:\n· молочный беж\n· шоколад\n· чёрный\n· зелёный\n\nРазмеры:\nS–M (42–44)\nL–XL (46–48)\n2XL–3XL (50–52)\n\nТепло × Стиль × Комфорт в одном платье 🫶\nИдеально с сапогами, кроссовками или лодочками — от прогулки до свидания и маленького праздника 💃",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
            {"name": "Платье Evening Mood", "price": "1890 грн", "description": "Для особых случаев."},
            {"name": "Платье Cozy Flow", "price": "1590 грн", "desc": "Комфорт и уют."},
        ],
    },
    "suits": {
        "title": "🧥 Костюмы",
        "items": [
            {"name": "Костюм Urban Chic", "price": "2490 грн", "description": "Стиль на каждый день."},
            {"name": "Костюм Soft Office", "price": "2690 грн", "description": "Элегантный образ."},
            {"name": "Костюм Relax Fit", "price": "2390 грн", "desc": "Свободный крой."},
        ],
    },
    "lingerie": {
        "title": "🩱 Нижнее бельё",
        "items": [
            {"name": "Комплект Silk Touch", "price": "1290 грн", "description": "Нежный и комфортный."},
            {"name": "Комплект Lace Mood", "price": "1390 грн", "description": "Женственный акцент."},
            {"name": "Комплект Soft Basic", "price": "1190 грн", "description": "На каждый день."},
        ],
    },
    "outerwear": {
        "title": "🧥 Верхняя одежда",
        "items": [
            {"name": "Пальто Soft City", "price": "3490 грн", "description": "Минимализм и тепло."},
            {"name": "Куртка Cozy Air", "price": "2990 грн", "description": "Лёгкая и удобная."},
            {"name": "Жакет Elegant Line", "price": "2790 грн", "description": "Завершённый образ."},
        ],
    },
}

# ---- START ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Добро пожаловать в Soft Mood 🤍\n\n"
        "Мы — магазин женской одежды.\n"
        "Поможем подобрать образ и оформить заказ.\n\n"
        "Выберите категорию 👇"
    )

    keyboard = [
        [InlineKeyboardButton("👗 Женская одежда", callback_data="women")]
    ]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# ---- ПОКАЗ ТОВАРА ----
async def show_item(query, context):
    category_key = context.user_data["category"]
    index = context.user_data["item_index"]

    category = CATEGORIES[category_key]
    item = category["items"][index]

    text = (
        f"{category['title']}\n\n"
        f"✨ {item['name']}\n"
        f"💰 {item['price']}\n\n"
        f"{item['descriptionc']}"
    )

    keyboard = [
        [InlineKeyboardButton("🛍 Заказать", callback_data="order")],
        [InlineKeyboardButton("➡️ Следующий товар", callback_data="next_item")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_categories")],
    ]

    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# ---- КНОПКИ ----
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "women":
        keyboard = [
            [InlineKeyboardButton("👗 Платья", callback_data="dresses")],
            [InlineKeyboardButton("🧥 Костюмы", callback_data="suits")],
            [InlineKeyboardButton("🩱 Нижнее бельё", callback_data="lingerie")],
            [InlineKeyboardButton("🧥 Верхняя одежда", callback_data="outerwear")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_start")],
        ]
        await query.message.reply_text(
            "Выберите категорию 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif data in CATEGORIES:
        context.user_data["category"] = data
        context.user_data["item_index"] = 0
        await show_item(query, context)

    elif data == "next_item":
        category = CATEGORIES[context.user_data["category"]]
        context.user_data["item_index"] = (
            context.user_data["item_index"] + 1
        ) % len(category["items"])
        await show_item(query, context)

    elif data == "order":
        context.user_data["waiting_for_phone"] = True
        await query.message.reply_text(
            "Спасибо 💛\n\nНапишите ваш номер телефона — менеджер свяжется с вами."
        )

    elif data == "back_to_categories":
        await buttons(
            Update(update.update_id, callback_query=query._replace(data="women")),
            context,
        )

    elif data == "back_to_start":
        await start(query.message, context)

# ---- ПРИЁМ ТЕЛЕФОНА ----
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_phone"):
        phone = update.message.text
        category = CATEGORIES[context.user_data["category"]]
        item = category["items"][context.user_data["item_index"]]

        order_text = (
            "🛍 НОВЫЙ ЗАКАЗ\n\n"
            f"📂 Категория: {category['title']}\n"
            f"✨ Товар: {item['name']}\n"
            f"💰 Цена: {item['price']}\n"
            f"📞 Телефон: {phone}\n"
            "📍 Город: Киев\n"
            "🚚 Новая почта — наложенный платёж"
        )

        await context.bot.send_message(chat_id=OWNER_ID, text=order_text)

        await update.message.reply_text(
            "Спасибо 🤍\n"
            "Мы свяжемся с вами в ближайшее время 🌷"
        )

        context.user_data["waiting_for_phone"] = False

# ---- ЗАПУСК ----
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT, handle_text))
app.run_polling()
