from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio

# -------------------------
# تنظیمات
# -------------------------
TOKEN = "8838744628:AAHvYnUw1FGel9jXP7sUVGy3IRXGKW93pGg"

CHAT_ID = -1003792979415
TOPIC1_ID = 7
TOPIC2_ID = 8

LINK_TOPIC1 = "https://x.com/Mr_CryptoNest/status/2064306977551896970   dont skip/ following first"
LINK_TOPIC2 = "https://x.com/Mr_CryptoNest/status/2063619155715109250 skip=mute"

last_msg_1 = None
last_msg_2 = None

bot = Bot(TOKEN)

# -------------------------
# تغییر لینک‌ها از تلگرام
# -------------------------
async def setlink1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global LINK_TOPIC1

    if context.args:
        LINK_TOPIC1 = " ".join(context.args)
    else:
        await update.message.reply_text("❌ enter link")

async def setlink2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global LINK_TOPIC2

    if context.args:
        LINK_TOPIC2 = " ".join(context.args)
    else:
        await update.message.reply_text("❌ enter link")

# -------------------------
# سیستم هشدار + حذف پیام کاربر (فقط دو تاپیک)
# -------------------------
async def warn_and_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = update.message

        if not msg:
            return

        # 👇 فقط داخل دو تاپیک فعال باشد
        thread_id = msg.message_thread_id

        if thread_id not in [TOPIC1_ID, TOPIC2_ID]:
            return

        # ارسال هشدار
        warn_msg = await msg.reply_text(
            "⚠️ following the rules in the group"
        )

        # حذف پیام کاربر
        # await msg.delete()

        # صبر 2 ثانیه
        await asyncio.sleep(2)

        # حذف پیام هشدار
        await warn_msg.delete()

    except Exception as e:
        print("Warn error:", e)

# -------------------------
# حلقه ارسال خودکار
# -------------------------
async def send_loop():
    global last_msg_1, last_msg_2

    while True:
        try:
            # تاپیک 1
            if last_msg_1:
                try:
                    await bot.delete_message(CHAT_ID, last_msg_1)
                except:
                    pass

            msg1 = await bot.send_message(
                chat_id=CHAT_ID,
                text=f"📌 Admin:\n{LINK_TOPIC1}",
                message_thread_id=TOPIC1_ID
            )
            last_msg_1 = msg1.message_id

            # تاپیک 2
            if last_msg_2:
                try:
                    await bot.delete_message(CHAT_ID, last_msg_2)
                except:
                    pass

            msg2 = await bot.send_message(
                chat_id=CHAT_ID,
                text=f"📌 Admin:\n{LINK_TOPIC2}",
                message_thread_id=TOPIC2_ID
            )
            last_msg_2 = msg2.message_id

            print("✔ message sent")

        except Exception as e:
            print("خطا:", e)

        await asyncio.sleep(300)  # 5 دقیقه

# -------------------------
# post init
# -------------------------
async def post_init(app: Application):
    asyncio.create_task(send_loop())

# -------------------------
# main
# -------------------------
def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()

    # دستورات تغییر لینک
    app.add_handler(CommandHandler("setlink1", setlink1))
    app.add_handler(CommandHandler("setlink2", setlink2))

    # 👇 فقط پیام‌های دو تاپیک
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, warn_and_delete))

    print("🤖 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()