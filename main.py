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
    "name": "Платье Evening Mood",
    "price": "1890 грн",
    "description": "Для особых случаев 🤍",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
            {
    "name": "Платье Evening Mood",
    "price": "1890 грн",
    "description": "Для особых случаев 🤍",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
            {
    "name": "Платье Evening Mood",
    "price": "1890 грн",
    "description": "Для особых случаев 🤍",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
    },
    "suits": {
        "title": "🧥 Костюмы",
        "items": [
            {
    "name": "Платье Evening Mood",
    "price": "1890 грн",
    "description": "Для особых случаев 🤍",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
            {
    "name": "Платье Evening Mood",
    "price": "1890 грн",
    "description": "Для особых случаев 🤍",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
            {
    "name": "Платье Evening Mood",
    "price": "1890 грн",
    "description": "Для особых случаев 🤍",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
        ],
    },
    "lingerie": {
        "title": "🩱 Нижнее бельё",
        "items": [
            {
    "name": "Платье Evening Mood",
    "price": "1890 грн",
    "description": "Для особых случаев 🤍",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
            {
    "name": "Платье Evening Mood",
    "price": "1890 грн",
    "description": "Для особых случаев 🤍",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
            {
    "name": "Платье Evening Mood",
    "price": "1890 грн",
    "description": "Для особых случаев 🤍",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
        ],
    },
    "outerwear": {
        "title": "🧥 Верхняя одежда",
        "items": [
            {
    "name": "Платье Evening Mood",
    "price": "1890 грн",
    "description": "Для особых случаев 🤍",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
            {
    "name": "Платье Evening Mood",
    "price": "1890 грн",
    "description": "Для особых случаев 🤍",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
            {
    "name": "Платье Evening Mood",
    "price": "1890 грн",
    "description": "Для особых случаев 🤍",
    "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg"
},
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
