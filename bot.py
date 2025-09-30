import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ================================
# Yaha apni keys daalo
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
# ================================

# /start command - intro message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello sir/mem. I am a special chatbot made by *Mr. Anonymous*.\nAap kaise ho?",
        parse_mode="Markdown"
    )

# /end command - chat end message
async def end_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Chat end ho gaya hai. Phir milte hain! 👋",
        parse_mode="Markdown"
    )

# AI reply using OpenAI REST API
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    # Agar user /end command bhej de
    if user_msg.lower() == "/end":
        await end_chat(update, context)
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
        reply += "\n\n— Bot powered by Mr. Anonymous"
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Error: " + str(e))

# Main bot setup
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("end", end_chat))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    print("🤖 Bot started... Press CTRL+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
