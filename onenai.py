import os
import traceback
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from dotenv import load_dotenv
load_dotenv()

# Прямо указываем токен Telegram и OpenAI API
telegram_token = os.getenv("TELEGRAM_TOKEN")  # Замените на ваш токен Telegram
openai_api_key = os.getenv("OPENAI")  # Замените на ваш API ключ OpenAI


# Инициализация клиента OpenAI
openai.api_key = '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'

# Функция для начала общения с ботом
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Отправь мне предложение, и я помогу с его обработкой.")

# Функция для отправки длинных сообщений частями
async def send_long_message(update: Update, text: str) -> None:
    max_message_length = 4096
    for i in range(0, len(text), max_message_length):
        await update.message.reply_text(text[i:i + max_message_length])

# Функция обработки сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
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
        # Вызов OpenAI API для генерации текста (новая версия API)
        response = openai.completions.create(
            model="gpt-3.5-turbo",  # Указываем модель
            prompt=user_message,  # Сообщение пользователя
            max_tokens=150  # Опциональный параметр для контроля длины ответа
        )

        # Извлекаем текст ответа
        generated_text = response['choices'][0]['text'].strip()

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

    # Регистрация обработчика команды '/start'
    application.add_handler(CommandHandler("start", start))

    # Регистрация обработчика для всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота с polling
    application.run_polling()

if __name__ == '__main__':
    main()
