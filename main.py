import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
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
        [InlineKeyboardButton("👗 Женская одежда", callback_data="women")]
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- обработка кнопок ---
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "women":
        keyboard = [
            [InlineKeyboardButton("👗 Платья", callback_data="dresses")],
            [InlineKeyboardButton("🩱 Нижнее бельё", callback_data="lingerie")],
            [InlineKeyboardButton("🧥 Костюмы", callback_data="suits")],
            [InlineKeyboardButton("🧥 Верхняя одежда", callback_data="outerwear")],
        ]

        await query.message.reply_text(
            "Выберите категорию 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# --- запуск ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
