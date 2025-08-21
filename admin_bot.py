import logging
import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== CONFIG ==========
BOT_TOKEN = "7636476146:AAFl2JDniUNsQYRFsU6BSHPVyS8sqQn0ejg"
ADMIN_CHAT_ID = 6800292901
GIST_ID = "426a9400569f40b6f4d664b74801a78a"

PART1 = "github_pat_11BQYPIPI0boMKyo1ZCgKa_"
PART2 = "LMmfMm9vacbpv1upw9PQ1mT7l2DQ3r24JD"
PART3 = "eTOOz1o5ePTEH7RT4RE861P9f"

GITHUB_PAT = PART1 + PART2 + PART3
HEADERS = {"Authorization": f"token {GITHUB_PAT}"}
GIST_URL = f"https://api.github.com/gists/{GIST_ID}"
# ============================

logging.basicConfig(level=logging.INFO)

def load_transactions():
    r = requests.get(GIST_URL, headers=HEADERS).json()
    files = r.get("files", {})
    content = files.get("transactions.json", {}).get("content", "{}")
    return json.loads(content)

def save_transactions(data):
    payload = {"files": {"transactions.json": {"content": json.dumps(data, indent=2)}}}
    requests.patch(GIST_URL, headers=HEADERS, json=payload)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_CHAT_ID:
        return
    txns = load_transactions()
    buttons = []
    for utr, info in txns.items():
        if info["status"] == "pending":
            buttons.append([InlineKeyboardButton(f"UTR {utr}", callback_data=f"utr_{utr}")])
    if not buttons:
        await update.message.reply_text("No pending UTRs.")
    else:
        await update.message.reply_text("Pending UTRs:", reply_markup=InlineKeyboardMarkup(buttons))

async def handle_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    utr = query.data.replace("utr_", "")
    txns = load_transactions()
    if utr not in txns:
        await query.edit_message_text("UTR not found.")
        return
    keyboard = [
        [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{utr}")],
        [InlineKeyboardButton("❌ Decline", callback_data=f"decline_{utr}")]
    ]
    await query.edit_message_text(f"UTR: {utr}\nUser ID: {txns[utr]['user_id']}", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, utr = query.data.split("_", 1)
    txns = load_transactions()
    if utr not in txns:
        await query.edit_message_text("UTR not found.")
        return
    txns[utr]["status"] = "approved" if action == "approve" else "declined"
    save_transactions(txns)
    await query.edit_message_text(f"UTR {utr} has been {txns[utr]['status'].upper()}.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_utr, pattern="^utr_"))
    app.add_handler(CallbackQueryHandler(handle_action, pattern="^(approve|decline)_"))
    app.run_polling()

if __name__ == "__main__":
    main()
