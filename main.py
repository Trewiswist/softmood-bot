import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Добро пожаловать в Soft Mood 🤍\n\n"
        "Мы — магазин женской одежды.\n"
        "Здесь вы можете спокойно подобрать образ,\n"
        "оставить заявку и связаться с менеджером\n"
        "для уточнения размеров и деталей.\n\n"
        "Выберите, что вас интересует 👇"
    )

    keyboard = [
        ["👗 Женская одежда"]
    ]

    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

# --- категории ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if user_text == "👗 Женская одежда":
        keyboard = [
            ["👗 Платья"],
            ["🩱 Нижнее бельё"],
            ["🧥 Костюмы"],
            ["🧥 Верхняя одежда"],
            ["🔙 Назад"],
        ]

        await update.message.reply_text(
            "Выберите категорию 👇",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

    elif user_text == "🔙 Назад":
        await start(update, context)

    else:
        await update.message.reply_text("Я рядом 🤍")

# --- запуск ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
