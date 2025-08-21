import logging, requests, json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIG ---
ADMIN_BOT_TOKEN = "7636476146:AAFl2JDniUNsQYRFsU6BSHPVyS8sqQn0ejg"
ADMIN_CHAT_ID = 6800292901
GIST_ID = "426a9400569f40b6f4d664b74801a78a"
PART1 = "github_pat_11BQYPIPI0rMEipIqtHj9h"
PART2 = "_vmPF0bBNpQa1F46Er4SaZHWtvQbznPNoh"
PART3 = "D9krhomlbKOPCYCJNUxpcAMUnh"
GITHUB_PAT = PART1 + PART2 + PART3
GIST_URL = f"https://api.github.com/gists/{GIST_ID}"
HEADERS = {"Authorization": f"token {GITHUB_PAT}"}

logging.basicConfig(level=logging.INFO)

def load_transactions():
    r = requests.get(GIST_URL, headers=HEADERS).json()
    content = r.get("files", {}).get("transactions.json", {}).get("content", "{}")
    return json.loads(content)

def save_transactions(data):
    payload = {"files": {"transactions.json": {"content": json.dumps(data, indent=2)}}}
    requests.patch(GIST_URL, headers=HEADERS, json=payload)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_CHAT_ID:
        return
    await update.message.reply_text("Welcome Admin! Use /pending to see all UTRs.")

async def show_pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_CHAT_ID:
        return
    txns = load_transactions()
    for utr, data in txns.items():
        if data["status"] == "pending":
            keyboard = [
                [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{utr}")],
                [InlineKeyboardButton("❌ Decline", callback_data=f"decline_{utr}")]
            ]
            await update.message.reply_text(f"UTR: {utr}\nUser: {data['user_id']}",
                                            reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, utr = query.data.split("_")

    txns = load_transactions()
    if utr not in txns:
        await query.edit_message_text("UTR not found")
        return

    txns[utr]["status"] = "approved" if action == "approve" else "declined"
    user_id = txns[utr]["user_id"]
    save_transactions(txns)

    # Notify admin
    await query.edit_message_text(f"UTR {utr} marked as {txns[utr]['status']}")

    # Notify user
    if action == "approve":
        msg = "✅ Approved! You will receive your CC within 24 hours."
    else:
        msg = "❌ Declined! Wrong UTR. Contact support: @alone120122"

    await context.bot.send_message(chat_id=user_id, text=msg)

def main():
    app = Application.builder().token(ADMIN_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pending", show_pending))
    app.add_handler(CallbackQueryHandler(handle_action))
    app.run_polling()

if __name__ == "__main__":
    main()
