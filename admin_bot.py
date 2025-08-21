import logging
import requests
import json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== CONFIG ==========
BOT_TOKEN = "7636476146:AAFl2JDniUNsQYRFsU6BSHPVyS8sqQn0ejg"  # Admin bot token
ADMIN_ID = 6800292901
GIST_ID = "426a9400569f40b6f4d664b74801a78a"

PART1 = "github_pat_11BQYPIPI0rMEipIqtHj9h"
PART2 = "_vmPF0bBNpQa1F46Er4SaZHWtvQbznPNoh"
PART3 = "D9krhomlbKOPCYCJNUxpcAMUnh"
GITHUB_PAT = PART1 + PART2 + PART3

GIST_URL = f"https://api.github.com/gists/{GIST_ID}"
HEADERS = {"Authorization": f"token {GITHUB_PAT}"}
# ============================

logging.basicConfig(level=logging.INFO)

# --- Gist Helpers ---
def load_transactions():
    try:
        r = requests.get(GIST_URL, headers=HEADERS).json()
        files = r.get("files", {})
        content = files.get("transactions.json", {}).get("content", "{}")
        return json.loads(content)
    except Exception:
        return {}

def save_transactions(data):
    payload = {"files": {"transactions.json": {"content": json.dumps(data, indent=2)}}}
    requests.patch(GIST_URL, headers=HEADERS, json=payload)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_ID:
        return
    await update.message.reply_text("Admin bot ready. Use /pending to see pending UTRs.")

async def pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_ID:
        return
    txns = load_transactions()
    buttons = []
    for utr, info in txns.items():
        if info["status"] == "pending":
            buttons.append([InlineKeyboardButton(f"Approve {utr}", callback_data=f"approve_{utr}")])
            buttons.append([InlineKeyboardButton(f"Decline {utr}", callback_data=f"decline_{utr}")])
    if not buttons:
        await update.message.reply_text("No pending transactions.")
    else:
        await update.message.reply_text("Pending UTRs:", reply_markup=InlineKeyboardMarkup(buttons))

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    txns = load_transactions()
    action, utr = query.data.split("_")
    if utr not in txns:
        await query.edit_message_text("UTR not found.")
        return

    user_id = txns[utr]["user_id"]
    if action == "approve":
        txns[utr]["status"] = "approved"
        msg = "✅ Approved! You will receive your CC within 24 hours."
        keyboard = [[InlineKeyboardButton("📞 Contact Support", url="https://t.me/alone120122")]]
        context.bot.send_message(chat_id=user_id, text=msg, reply_markup=InlineKeyboardMarkup(keyboard))
        await query.edit_message_text(f"Approved {utr}")
    elif action == "decline":
        txns[utr]["status"] = "declined"
        msg = "❌ Declined. Contact support below."
        keyboard = [[InlineKeyboardButton("📞 Contact Support", url="https://t.me/alone120122")]]
        context.bot.send_message(chat_id=user_id, text=msg, reply_markup=InlineKeyboardMarkup(keyboard))
        await query.edit_message_text(f"Declined {utr}")

    save_transactions(txns)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pending", pending))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.run_polling()

if __name__ == "__main__":
    main()
