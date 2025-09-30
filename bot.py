# bot.py
import os
import requests
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# --- Helper: try load simple key-file if env vars not set ---
def load_from_file_if_needed():
    # अगर already set हैं तो कुछ नहीं करना
    if os.getenv("TELEGRAM_TOKEN") and os.getenv("OPENAI_API_KEY"):
        return

    path = Path.home() / ".openai_env"   # तुम जो फाइल बनाते हो: ~/.openai_env
    if not path.exists():
        return

    try:
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # handle lines like: export KEY="value"  या  KEY="value"  या KEY=value
            if line.startswith("export "):
                line = line[len("export "):]
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                # only set in env if not already present
                if not os.getenv(key):
                    os.environ[key] = val
    except Exception:
        # fail silently — program will detect missing vars later
        pass

# load fallback file (if needed)
load_from_file_if_needed()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise SystemExit("Error: TELEGRAM_TOKEN or OPENAI_API_KEY not set. Use `export` or create ~/.openai_env")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello sir/mem. I am a special chatbot made by *Mr. Anonymous*.\nAap kaise ho?",
        parse_mode="Markdown"
    )

# /end command
async def end_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chat end ho gaya hai. Phir milte hain! 👋", parse_mode="Markdown")

# AI reply
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    if not user_msg:
        return
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
        "messages": [{"role": "user", "content": user_msg}],
        "max_tokens": 600
    }

    try:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        j = resp.json()
        reply = j["choices"][0]["message"]["content"].strip()
        reply += "\n\n— Bot powered by Mr. Anonymous"
        await update.message.reply_text(reply)
    except Exception as e:
        # don't leak tokens in error logs
        await update.message.reply_text("Error contacting OpenAI: " + str(e))

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("end", end_chat))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))
    print("🤖 Bot started... Press CTRL+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
