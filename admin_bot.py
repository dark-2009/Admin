import logging, requests, json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIG ---
BOT_TOKEN = "7636476146:AAFl2JDniUNsQYRFsU6BSHPVyS8sqQn0ejg"
ADMIN_ID = 6800292901  # your chat id

# same split PAT for safety
PART1 = "github_pat_11BQYPIPI0rMEipIqtH9h"
PART2 = "_vmPF0bBNpQa1F46Er4SaZHWtvQbznPNoh"
PART3 = "D9krhomlbKOPCYCJNUxpcAMUnh"
GITHUB_PAT = PART1 + PART2 + PART3

GIST_ID = "426a9400569f40b6f4d664b74801a78a"
GIST_URL = f"https://api.github.com/gists/{GIST_ID}"
HEADERS = {"Authorization": f"token {GITHUB_PAT}"}

logging.basicConfig(level=logging.INFO)

# --- Gist Helpers ---
def load_transactions():
    r = requests.get(GIST_URL, headers=HEADERS).json()
    content = r.get("files", {}).get("transactions.json", {}).get("content", "{}")
    return json.loads(content)

def save_transactions(data):
    payload = {"files": {"transactions.json": {"content": json.dumps(data, indent=2)}}}
    requests.patch(GIST_URL, headers=HEADERS, json=payload)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_ID:
        await update.message.reply_text("⛔ Unauthorized.")
        return
    await update.message.reply_text("Welcome Admin! Use /pending to see UTRs.")

async def show_pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_ID:
        return

    txns = load_transactions()
    pending = [utr for utr, info in txns.items() if info["status"] == "pending"]

    if not pending:
        await update.message.reply_text("✅ No pending UTRs.")
        return

    for utr in pending:
        user_id = txns[utr]["user_id"]
        keyboard = [
            [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{utr}")],
            [InlineKeyboardButton("❌ Decline", callback_data=f"decline_{utr}")]
        ]
        await update.message.reply_text(
            f"UTR: `{utr}`\nUser ID: `{user_id}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query.message.chat_id != ADMIN_ID:
        return

    query = update.callback_query
    await query.answer()

    action, utr = query.data.split("_")
    txns = load_transactions()
    if utr not in txns:
        await query.edit_message_text("UTR not found.")
        return

    if action == "approve":
        txns[utr]["status"] = "approved"
        msg = f"✅ Approved UTR {utr}"
    else:
        txns[utr]["status"] = "declined"
        msg = f"❌ Declined UTR {utr}"

    save_transactions(txns)
    await query.edit_message_text(msg)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pending", show_pending))
    app.add_handler(CallbackQueryHandler(handle_action))
    app.run_polling()

if __name__ == "__main__":
    main()
