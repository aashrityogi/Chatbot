import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Telegram aur OpenAI tokens
TELEGRAM_TOKEN = "8031671164:AAHQUTF-RN7_GP_MinE7UQVy0ZVkbQkzapg"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

# Start command
def start(update, context):
    update.message.reply_text(
        "Hello sir/mem. I am a special chatbot made by *Mr. Anonymous*.\nAap kaise ho?",
        parse_mode="Markdown"
    )

# End command
def end_chat(update, context):
    update.message.reply_text(
        "Chat end ho gaya hai. Phir milte hain! 👋",
        parse_mode="Markdown"
    )

# AI auto-reply function
def ai_reply(update, context):
    user_msg = update.message.text

    # Agar user ne /end nahi diya
    if user_msg.lower() == "/end":
        end_chat(update, context)
        return

    try:
        # OpenAI se reply le
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_msg}]
        )
        reply = response["choices"][0]["message"]["content"]

        # Bot reply ke end me ye add kar rahe
        reply += "\n\n— Bot powered by Mr. Anonymous"

        update.message.reply_text(reply)

    except Exception as e:
        update.message.reply_text("Error: " + str(e))

# Main bot setup
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("end", end_chat))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ai_reply))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
