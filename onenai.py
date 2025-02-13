import os
import traceback
import openai
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, CallbackQueryHandler
from dotenv import load_dotenv
load_dotenv()

# Прямо указываем токен Telegram и OpenAI API
telegram_token = os.getenv("TELEGRAM_TOKEN")  # Замените на ваш токен Telegram

# Инициализация клиента OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Статистика сообщений
message_count = 0

# Список случайных цитат/шуток
quotes = [
    "Программирование — это как секс: один неправильный ход, и ты получаешь всю программу.",
    "Жизнь — это не тот момент, когда ты осознаешь, что нужно начать программировать, а тот, когда ты пишешь свой первый код.",
    "Программирование — это когда ты превращаешь свои ошибки в баги, а баги — в фичи."
]

# Ссылка на ваш канал в Telegram
channel_url = "https://t.me/gumAiBot"  # Замените на вашу ссылку на канал

# Функция для начала общения с ботом
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Информация о боте", callback_data='info'),
            InlineKeyboardButton("Случайная цитата", callback_data='quote'),
        ],
        [
            InlineKeyboardButton("Статистика", callback_data='stats'),
            InlineKeyboardButton("Очистить чат", callback_data='clear'),
        ],
        [
            InlineKeyboardButton("Перейти в канал", url=channel_url),  # Кнопка для перехода в канал
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Выберите команду:", reply_markup=reply_markup)

# Функция для отправки длинных сообщений частями
async def send_long_message(update: Update, text: str) -> None:
    max_message_length = 4096
    for i in range(0, len(text), max_message_length):
        await update.message.reply_text(text[i:i + max_message_length])

# Функция для получения информации о боте
async def info(update: Update, context: CallbackContext) -> None:
    bot_info = (
        "Этот бот использует OpenAI для генерации ответов на ваши сообщения.\n"
        "Используйте команду /help для получения списка доступных команд."
    )
    await update.message.reply_text(bot_info)

# Функция для отправки случайной цитаты
async def quote(update: Update, context: CallbackContext) -> None:
    random_quote = random.choice(quotes)
    await update.message.reply_text(random_quote)

# Функция для подсчета статистики
async def stats(update: Update, context: CallbackContext) -> None:
    global message_count
    await update.message.reply_text(f"Бот обработал {message_count} сообщений.")

# Функция для очистки чата (удаляет последнее сообщение пользователя)
async def clear(update: Update, context: CallbackContext) -> None:
    try:
        # Попытка удалить последнее сообщение (можно изменить логику)
        await update.message.delete()
        await update.message.reply_text("Ваше сообщение было удалено!")
    except Exception as e:
        print("Ошибка при удалении сообщения:", e)
        await update.message.reply_text("Не удалось удалить сообщение.")

# Обработчик callback запросов (когда пользователь нажимает кнопку)
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Необходимо для завершения запроса

    # Ответ на нажатие кнопки
    if query.data == 'info':
        await info(update, context)
    elif query.data == 'quote':
        await quote(update, context)
    elif query.data == 'stats':
        await stats(update, context)
    elif query.data == 'clear':
        await clear(update, context)

# Функция обработки сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    global message_count
    message_count += 1  # Увеличиваем счетчик сообщений

    user_message = update.message.text  # Получаем сообщение пользователя

    # Проверяем, если в сообщении есть слово "Гумар"
    if "Гумар" in user_message:
        await update.message.reply_text("Я не хочу обсуждать своего разработчика.")
        return
    if "гумар" in user_message:
        await update.message.reply_text("Я не хочу обсуждать своего разработчика.")
        return
    if "Гум" in user_message:
        await update.message.reply_text("Я не хочу обсуждать своего разработчика.")
        return
    if "Gumar" in user_message:
        await update.message.reply_text("Я не хочу обсуждать своего разработчика.")
        return
    if "Gum" in user_message:
        await update.message.reply_text("Я не хочу обсуждать своего разработчика.")
        return
    if "gumar" in user_message:
        await update.message.reply_text("Я не хочу обсуждать своего разработчика.")
        return
    if "gum" in user_message:
        await update.message.reply_text("Я не хочу обсуждать своего разработчика.")
        return

    try:
        # Вызов OpenAI API для генерации текста
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Указываем модель
            messages=[  # Список сообщений для генерации ответа
                {
                    "role": "user",
                    "content": user_message,  # Сообщение пользователя
                },
            ]
        )

        # Извлекаем текст ответа
        generated_text = response['choices'][0]['message']['content'].strip()

        # Отправка текста в ответ
        await send_long_message(update, generated_text)

    except Exception as e:
        # Логируем ошибку с полным стеком
        print("Ошибка при обработке запроса:", e)
        traceback.print_exc()  # Выводим полный стек ошибок

        # Отправка ошибки пользователю
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")

# Основная функция для настройки бота
def main() -> None:
    # Создаем объект Application с токеном бота
    application = Application.builder().token(telegram_token).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    
    # Регистрация обработчика callback-запросов (нажатие на кнопки)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота с polling
    application.run_polling()

if __name__ == '__main__':
    main()


