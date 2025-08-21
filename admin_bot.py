import logging, requests, json, asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========= CONFIG =========
BOT_TOKEN = "7636476146:AAFl2JDniUNsQYRFsU6BSHPVyS8sqQn0ejg"
ADMIN_ID = 6800292901
PART1 = "github_pat_11BQYPIPI0rMEipIqtH9h"
PART2 = "_vmPF0bBNpQa1F46Er4SaZHWtvQbznPNoh"
PART3 = "D9krhomlbKOPCYCJNUxpcAMUnh"
GITHUB_PAT = PART1 + PART2 + PART3

GIST_ID = "426a9400569f40b6f4d664b74801a78a"
GIST_URL = f"https://api.github.com/gists/{GIST_ID}"
HEADERS = {"Authorization": f"token {GITHUB_PAT}"}
# ==========================

logging.basicConfig(level=logging.INFO)

def load_transactions():
    r = requests.get(GIST_URL, headers=HEADERS).json()
    files = r.get("files", {})
    content = files.get("transactions.json", {}).get("content", "{}")
    return json.loads(content)

def save_transactions(data):
    payload = {"files": {"transactions.json": {"content": json.dumps(data, indent=2)}}}
    requests.patch(GIST_URL, headers=HEADERS, json=payload)

async def pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_ID:
        return
    txns = load_transactions()
    pendings = [utr for utr, d in txns.items() if d["status"] == "pending"]
    if not pendings:
        await update.message.reply_text("No pending UTRs.")
        return
    for utr in pendings:
        keyboard = [
            [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{utr}")],
            [InlineKeyboardButton("❌ Decline", callback_data=f"decline_{utr}")]
        ]
        await update.message.reply_text(f"UTR: {utr}", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.message.chat_id != ADMIN_ID:
        return

    action, utr = query.data.split("_")
    txns = load_transactions()
    if utr not in txns:
        await query.edit_message_text("UTR not found.")
        return

    txns[utr]["status"] = "approved" if action == "approve" else "declined"
    save_transactions(txns)

    await query.edit_message_text(f"UTR {utr} marked as {txns[utr]['status']}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("pending", pending))
    app.add_handler(CallbackQueryHandler(handle_admin_buttons))
    app.run_polling()

if __name__ == "__main__":
    main()
