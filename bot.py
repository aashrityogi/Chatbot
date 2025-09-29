import openai
from telegram.ext import Updater, MessageHandler, Filters

# Telegram aur OpenAI tokens
TELEGRAM_TOKEN = "APNA_TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY = "APNA_OPENAI_KEY"

openai.api_key = OPENAI_API_KEY

def ai_reply(update, context):
    user_msg = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_msg}]
        )

        reply = response["choices"][0]["message"]["content"]
        update.message.reply_text(reply)

    except Exception as e:
        update.message.reply_text("Error: " + str(e))

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ai_reply))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
