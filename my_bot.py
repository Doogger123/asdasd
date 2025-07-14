from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes, ConversationHandler
from openpyxl import Workbook, load_workbook
import os

TOKEN = "7603428852:AAHRS8vizKnQuFKJ3EShsMeLjgP3OM3PsYw"

ASK_NAME, ASK_AGE, ASK_DAY, ASK_TIME = range(4)
signups = []
ADMIN_ID = 2077512321

TRAINER_IDS = [2077512321, 669664459]  # ← сюда реальные ID тренеров

days = ["Понедельник", "Вторник", "Среда", "Четверг"]
times = ["9:00-10:30", "10:30-12:00", "15:00-16:30", "16:30-18:00"]

def save_to_excel(name, age, day, time):
    filename = "signups.xlsx"
    if not os.path.exists(filename):
        wb = Workbook()
        ws = wb.active
        ws.title = "Записи"
        ws.append(["ФИО", "Возраст", "День", "Время"])
    else:
        wb = load_workbook(filename)
        ws = wb.active

    ws.append([name, age, day, time])
    wb.save(filename)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👨‍💼 Руководство", callback_data="management")],
        [InlineKeyboardButton("🏋️‍♂️ Тренеры", callback_data="coaches")],
        [InlineKeyboardButton("🎮 Дисциплины", callback_data="disciplines")],
        [InlineKeyboardButton("✅ Записаться на занятие", callback_data="start_signup")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Привет! Добро пожаловать в наш центр компьютерного спорта!\n\nВыбери раздел:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "management":
        keyboard = [
            [InlineKeyboardButton("Председатель", callback_data="chairman")],
            [InlineKeyboardButton("Исполнительный директор", callback_data="executive")],
            [InlineKeyboardButton("Директор турниров", callback_data="tournament_director")],
            [InlineKeyboardButton("Администратор турниров", callback_data="tournament_admin")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Выбери руководителя:", reply_markup=reply_markup)

    elif query.data == "chairman":
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="management")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_photo(
            photo="https://i.imgur.com/FYfd7YA.jpg",
            caption="👨‍💼 **Председатель** — Надырханов Дмитрий Сергеевич",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "executive":
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="management")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_photo(
            photo="https://i.imgur.com/sBF4K9U.jpg",
            caption="👔 **Исполнительный директор** — Мелузов Константин Анатольевич",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "tournament_director":
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="management")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_photo(
            photo="https://i.ibb.co/JjmYjRNN/GUYZ5-Pe-MYe2-QV0-Tw-MMMvs-Ji-BGbyx-Ajo-GUK50-RKOEXh-Ycgf-O7pu5-Cp-Zuov5m5ih4lef-R7-CE35vj-XJAv-Hlc8.jpg",  # временная заставка
            caption="🏆 **Директор турниров** — Матюшкин Радик Маратович",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "tournament_admin":
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="management")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_photo(
            photo="https://i.imgur.com/LAeiXQx.jpg",
            caption="🗂 **Администратор турниров** — Мищенко Евгений Сергеевич",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "coaches":
        keyboard = [
            [InlineKeyboardButton("Главный тренер — Мелузов Константин", callback_data="head_coach")],
            [InlineKeyboardButton("Тренер по гонкам дронов — Мищенко Евгений", callback_data="drone_coach")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Выбери тренера:", reply_markup=reply_markup)

    elif query.data == "head_coach":
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="coaches")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_photo(
            photo="https://i.imgur.com/WmM5c87.jpg",
            caption="👨‍🏫 **Главный тренер** — Мелузов Константин\nСпециализация: CS 2.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "drone_coach":
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="coaches")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_photo(
            photo="https://i.imgur.com/LAeiXQx.jpg",
            caption="🚁 **Тренер по гонкам дронов** — Мищенко Евгений\nСпециализация: DCL.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "disciplines":
        keyboard = [
            [InlineKeyboardButton("Гонки дронов", callback_data="drones")],
            [InlineKeyboardButton("Боевая арена", callback_data="arena")],
            [InlineKeyboardButton("Соревновательные головоломки", callback_data="puzzles")],
            [InlineKeyboardButton("Стратегия в реальном времени", callback_data="rts")],
            [InlineKeyboardButton("Технический симулятор", callback_data="tech_sim")],
            [InlineKeyboardButton("Спортивный симулятор", callback_data="sport_sim")],
            [InlineKeyboardButton("Файтинг", callback_data="fighting")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Выбери дисциплину:", reply_markup=reply_markup)

    elif query.data in ["drones", "arena", "puzzles", "rts", "tech_sim", "sport_sim", "fighting"]:
        descriptions = {
            "drones": "🚁 **Гонки дронов** — гоночные соревнования FPV-квадрокоптеров на трассах.",
            "arena": "⚔ **Боевая арена** — командные сражения на карте с целью уничтожения базы противника.",
            "puzzles": "🧩 **Соревновательные головоломки** — решение логических задач на скорость.",
            "rts": "🕹 **Стратегия в реальном времени** — стратегия без ходов, всё происходит динамично.",
            "tech_sim": "🔧 **Технический симулятор** — имитация управления техникой по спортивным правилам.",
            "sport_sim": "⚽ **Спортивный симулятор** — видеоигра, имитирующая спортивные соревнования.",
            "fighting": "🥊 **Файтинг** — бои персонажей на арене, жанр видеоигр и дисциплина киберспорта.",
        }
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="disciplines")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(descriptions[query.data], reply_markup=reply_markup)

    elif query.data == "start_signup":
        await query.message.reply_text("Введите ваше ФИО:")
        context.user_data.clear()
        context.user_data["signup"] = True
        return ASK_NAME

    elif query.data == "back_main":
        await start(query, context)

async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("signup"):
        context.user_data["name"] = update.message.text
        await update.message.reply_text("Укажите ваш возраст:")
        return ASK_AGE

async def ask_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    keyboard = [[KeyboardButton(day)] for day in days]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите день недели:", reply_markup=reply_markup)
    return ASK_DAY

async def ask_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["day"] = update.message.text
    keyboard = [[KeyboardButton(time)] for time in times]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите время:", reply_markup=reply_markup)
    return ASK_TIME

async def confirm_signup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data["name"]
    age = context.user_data["age"]
    day = context.user_data["day"]
    time = update.message.text

    signups.append({"name": name, "age": age, "day": day, "time": time})
    save_to_excel(name, age, day, time)

    message = f"👤 Новая запись!\nФИО: {name}\nВозраст: {age}\nДень: {day}\nВремя: {time}"
    for trainer_id in TRAINER_IDS:
        await context.bot.send_message(chat_id=trainer_id, text=message)

    await update.message.reply_text(
        f"✅ Записал вас, {name} (возраст: {age}), на {day} в {time}.",
        reply_markup=ReplyKeyboardMarkup([["/start"]], resize_keyboard=True)
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Запись отменена ❌")
    return ConversationHandler.END

async def list_signups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("У тебя нет доступа 🚫")
        return
    if not signups:
        await update.message.reply_text("Пока никто не записался.")
        return
    text = "Список записавшихся:\n\n"
    for i, s in enumerate(signups, start=1):
        text += f"{i}. {s['name']} (возраст: {s['age']}) — {s['day']} в {s['time']}\n"
    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_signups))

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern="^start_signup$")],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_day)],
            ASK_DAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_time)],
            ASK_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_signup)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()

