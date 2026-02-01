import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

# ---- ТЕСТОВЫЕ ПЛАТЬЯ ----
DRESSES = [
    {
        "name": "Платье Soft Line",
        "price": "1690 грн",
        "desc": "Лёгкое женственное платье на каждый день. Мягкая ткань, комфортная посадка."
    },
    {
        "name": "Платье Evening Mood",
        "price": "1890 грн",
        "desc": "Элегантное платье для особых случаев. Подчёркивает фигуру."
    },
    {
        "name": "Платье Cozy Flow",
        "price": "1590 грн",
        "desc": "Уютное платье свободного кроя. Идеально для прогулок."
    },
]

# ---- START ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Добро пожаловать в Soft Mood 🤍\n\n"
        "Мы — магазин женской одежды.\n"
        "Здесь вы можете спокойно подобрать образ,\n"
        "оставить заявку и связаться с менеджером.\n\n"
        "Выберите, что вас интересует 👇"
    )

    keyboard = [
        [InlineKeyboardButton("👗 Женская одежда", callback_data="women")]
    ]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# ---- ПОКАЗ ПЛАТЬЯ ----
async def show_dress(query, context, index):
    dress = DRESSES[index]
    context.user_data["dress_index"] = index

    text = (
        f"👗 {dress['name']}\n"
        f"💰 {dress['price']}\n\n"
        f"{dress['desc']}"
    )

    keyboard = [
        [InlineKeyboardButton("🛍 Заказать", callback_data="order")],
        [InlineKeyboardButton("➡️ Следующее платье", callback_data="next_dress")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_categories")]
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
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_start")]
        ]
        await query.message.reply_text(
            "Выберите категорию 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "dresses":
        await show_dress(query, context, 0)

    elif data == "next_dress":
        index = context.user_data.get("dress_index", 0)
        index = (index + 1) % len(DRESSES)
        await show_dress(query, context, index)

    elif data == "order":
        await query.message.reply_text(
            "Спасибо 💛\n\nНапишите, пожалуйста, ваш номер телефона — менеджер свяжется с вами для уточнения деталей."
        )

    elif data == "back_to_categories":
        keyboard = [
            [InlineKeyboardButton("👗 Платья", callback_data="dresses")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_start")]
        ]
        await query.message.reply_text(
            "Выберите категорию 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "back_to_start":
        await start(query.message, context)

# ---- ЗАПУСК ----
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.run_polling()
