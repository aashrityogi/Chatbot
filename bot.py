import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# ================================
# Yaha apni keys daalo
TELEGRAM_TOKEN = "APNA_TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY = "APNA_OPENAI_KEY"
# ================================

# /start command - intro message
def start(update, context):
    update.message.reply_text(
        "Hello sir/mem. I am a special chatbot made by *Mr. Anonymous*.\nAap kaise ho?",
        parse_mode="Markdown"
    )

# /end command - chat end message
def end_chat(update, context):
    update.message.reply_text(
        "Chat end ho gaya hai. Phir milte hain! 👋",
        parse_mode="Markdown"
    )

# AI reply using REST API
def ai_reply(update, context):
    user_msg = update.message.text

    # Agar user /end command bhej de
    if user_msg.lower() == "/end":
        end_chat(update, context)
        return

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_msg}]
    }

    try:
        response = requests.post(url, headers=headers, json=data).json()
        reply = response["choices"][0]["message"]["content"]
        # Reply ke end me signature
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
