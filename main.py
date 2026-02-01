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

# ================== КАТЕГОРИИ И ТОВАРЫ ==================

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
            {
    "name": "Базовое тёплое платье с акцентом на талии 🖤✨ Мод. 368",
    "price": "742 ₴",
    "description": "То самое платье, которое хочется носить каждый день! 🫶\n\n• Очень мягкая и тёплая ангора\n• Съёмный пояс — подчёркивает талию\n• Удобная мини-длина\n• Круглый вырез + длинный рукав\n\nДоступные цвета:\n🖤 чёрный   🍓 малина   🌿 зелёный\n💙 синий   ❤️ красный   🥛 молочный\n\nРазмеры: 42-44 • 46-48 • 50-52\n\nПоясок уже в комплекте 🎁\nГотово к холодным дням и комплиментам! ❄️💃",
    "photo": "https://images.prom.ua/7025587121_w640_h640_bazovoe-teploe-plate.jpg"
},
            {
    "name": "Чёрное платье миди с открытыми плечами 🖤👗",
    "price": "800 ₴",
    "description": "Когда хочется выглядеть женственно, элегантно и чуточку соблазнительно… 😘\n\nЭто то самое платье:\n✨ глубокий чёрный цвет\n✨ сексуальные открытые плечи\n✨ приталенный силуэт, который красиво обнимает фигуру\n✨ мягкий, эластичный турецкий трикотаж\n✨ тянется и подходит на размеры S, M, L, XL\n\nДлина по спинке ≈ 129 см\nРукав 66 см\n\nОт прогулки по городу до романтического вечера – везде будет на высоте 💅\n\nЦвет: чёрный\nПроизводство: Турция\n\nТвоя идеальная база на все случаи! 🖤",
    "photo": "https://images.prom.ua/7006727327_w640_h640_zhenskoe-trikotazhnoe-plate.jpg"
},
        ],
    },

    "suits": {
        "title": "🧥 Костюмы",
        "items": [
            {
    "name": "Женский летний костюм ХАКИ (SM | L-XL)",
    "price": "1197 ₴",
    "description": "Код: OV-#573X\n\n✨ Лёгкий костюм-двойка на лето\nРубашка + брюки клёш\n\nХарактеристики:\n🌿 Ткань: американский креп-жатка\n🎨 Цвет: Хаки\n📏 Размеры: SM (42-46)  |  L-XL (48-50)\n\nРазмеры по телу:\nГрудь → 108 см (SM) / 116 см (L-XL)\nБёдра → 110 см (SM) / 120 см (L-XL)\n\nДлина рубашки 72 см\nДлина рукава 58 см\n\n🔥 Новый, качественный пошив\nСупер-удобный на каждый день и не только!",
    "photo": "https://images.prom.ua/4521912170_w640_h640_zhenskij-letnij-kostyum.jpg"
},
            {
    "name": "Нарядный темно-синий костюм 50-60 с блузой-сеткой ✨",
    "price": "1656 ₴",
    "description": "Готовый шикарный образ за 1 минуту! 💙\n\nПочему выбирают этот костюм:\n✔ Очень красивые рукава-сетка с флоком и серебром\n✔ Глубокий темно-синий — стройнит и выглядит дорого\n✔ Удобно сидит на пышной фигуре\n✔ Не мнётся, комфортно весь вечер\n✔ Блуза + брюки — комплект 2 в 1\n\nРазмеры в наличии:\n50-52 (ОГ 110 / ОБ 112)\n54-56 (ОГ 118 / ОБ 118)\n58-60 (ОГ 124 / ОБ 126)\n\nПовод: свадьба, юбилей, корпоратив, фотосессия, выпускной 🎉\nМатериал: креп-дайвинг + декоративная сетка\n\nБудь самой яркой на любом празднике! 🔥",
    "photo": "https://images.prom.ua/6887251372_w640_h640_zhenskij-bryuchnyj-kostyum.jpg"
},
            {
    "name": "Женский летний костюм ХАКИ (SM | L-XL)",
    "price": "1197 ₴",
    "description": "Код: OV-#573X\n\n✨ Лёгкий костюм-двойка на лето\nРубашка + брюки клёш\n\nХарактеристики:\n🌿 Ткань: американский креп-жатка\n🎨 Цвет: Хаки\n📏 Размеры: SM (42-46)  |  L-XL (48-50)\n\nРазмеры по телу:\nГрудь → 108 см (SM) / 116 см (L-XL)\nБёдра → 110 см (SM) / 120 см (L-XL)\n\nДлина рубашки 72 см\nДлина рукава 58 см\n\n🔥 Новый, качественный пошив\nСупер-удобный на каждый день и не только!",
    "photo": "https://images.prom.ua/4521912170_w640_h640_zhenskij-letnij-kostyum.jpg"
},
        ],
    },

    "lingerie": {
        "title": "🩱 Нижнее бельё",
        "items": [
            {
    "name": "Бралетт Lama L кружевной чёрный ✨ POL5023BR-02",
    "price": "655 ₴",
    "description": "🖤 Стильный бесшовный бралетт Lama – идеальный выбор для ежедневного комфорта и красоты!\n\n✨ Особенности:\n• Мягкий полиамид + красивое кружево\n• Без швов – не видно под одеждой\n• Лёгкая поддержка и естественная форма\n• Элегантная чёрная кружевная отделка\n\n🇵🇱 Производство: Польша\nРазмер: L\n\n💫 Комфорт + сексуальность в одном изделии!\n\nАртикул: 000161292",
    "photo": "https://images.prom.ua/4502660008_w640_h640_byustgalter-bralet-zhinochij-lama.jpg"
},
            {
    "name": "Колготки-термо «Вторая кожа» с пуш-ап утяжкой 🖤❄️",
    "price": "329 ₴",
    "description": "💫 Самые тёплые и при этом красивые колготки этой зимы!\n\n✨ Смотрятся как тонкий капрон, а греют как флисовые леггинсы\n🖤 Эффект «голых ног» + утягивающие трусики с пуш-ап\n🔥 Мягчайший флис внутри от талии до щиколотки\n🌟 Широкая эластичная резинка не скатывается\n\nРазмеры: 42-48 (бедра 85-100 см) и 48-52 (бедра 100-120 см)\nРост: комфортно 155–180 см\n\nВес 200 г → реально тёплые!\nЦвет: классический чёрный\n\nСтирать нежно при 40°C, без агрессивной химии и сушилки 🔥",
    "photo": "https://images.prom.ua/6305503920_w640_h640_teplye-zimnie-kolgotki.jpg"
},
            {
    "name": "Женский боди длинный рукав сетка-горох 989",
    "price": "900 ₴",
    "description": "🖤 Стильный чёрный боди – хит сезона!\n\nХарактеристики:\n🌟 Ткань: джерси + сетка горох\n🌟 Цвет: чёрный\n🌟 Рукав: длинный\n🌟 Вырез: соблазнительный\n\nРазмеры в наличии:\n→ 42-44 (S-M)\n→ 46-48 (L-XL)\n\nМодель: ОЛН 989\nЦена всего 900 грн 🔥\n\nПиши в Telegram/Viber 0684310362\nили заходи на https://in-butik.com.ua",
    "photo": "https://images.prom.ua/4194789985_w640_h640_zhenskij-bodi-s.jpg"
},
        ],
    },

    "outerwear": {
        "title": "🧥 Верхняя одежда",
        "items": [
            {
    "name": "Тёплая двухсторонняя шубка-тедди Шоколад 🧸🍫",
    "price": "2099 ₴",
    "description": "Обнимашки зимой? Теперь это возможно! 🤗\n\nДвухсторонняя мечта:\n✨ С одной стороны — невероятно мягкий и пушистый тедди\n✨ С другой — элегантная шоколадная плащевка\n\n105 см длины — тепло и красиво\nСиликон 250 — не боится морозов\nУютный капюшон, удобные карманы\n\nРазмеры: 42-44 и 46-48\nЦвет: глубокий шоколад 💞\n\nТакая вещь нужна каждой девушке этой зимой 🥰❄️",
    "photo": "https://images.prom.ua/6938046667_w640_h640_zhenskaya-zimnyaya-dvuhstoronnyaya.jpg"
},
            {
                "name": "Куртка Cozy Air",
                "price": "2990 грн",
                "description": "Лёгкая и удобная",
                "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg",
            },
            {
                "name": "Жакет Elegant Line",
                "price": "2790 грн",
                "description": "Завершённый образ ✨",
                "photo": "https://images.prom.ua/6878199359_w640_h640_plate-iz-dvustoronnego.jpg",
            },
        ],
    },
}

# ================== START ==================

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

# ================== ПОКАЗ ТОВАРА ==================

async def show_item(query, context):
    category_key = context.user_data["category"]
    index = context.user_data["item_index"]

    category = CATEGORIES[category_key]
    item = category["items"][index]

    text = (
        f"{category['title']}\n\n"
        f"✨ {item['name']}\n"
        f"💰 {item['price']}\n\n"
        f"{item['description']}"
    )

    keyboard = [
        [InlineKeyboardButton("🛍 Заказать", callback_data="order")],
        [InlineKeyboardButton("➡️ Следующий товар", callback_data="next_item")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_categories")],
    ]

    await query.message.reply_photo(
        photo=item["photo"],
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ================== КНОПКИ ==================

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
        await start(query.message, context)

    elif data == "back_to_start":
        await start(query.message, context)

# ================== ПРИЁМ ТЕЛЕФОНА ==================

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

# ================== ЗАПУСК ==================

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

app.run_polling()
