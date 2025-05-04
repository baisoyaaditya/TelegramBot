from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from collections import defaultdict

# Replace with your actual Bot Token from BotFather
TOKEN = "7265202909:AAEcAR4H626LegzNjpoV9uJGs4y3Kpm2mQY"
# In-memory storage for each user's missions
user_tasks = defaultdict(list)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Batcomputer, master Bruce.\nType /help to view your tools and commands."
    )

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Utility Commands:
    /batcave - Access the Batcave (YouTube)
    /wayne - Wayne Enterprises (LinkedIn)
    /alfred - Contact Alfred (Gmail)
    /oracle - Oracle's Surveillance Feed (Instagram)

Mission Manager:
    /mission add [task] - Add a mission
    /mission list - View your missions
    /mission done [number] - Complete a mission
    /mission clear - Clear all missions
""")

# Social links
async def gmail_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Contact Alfred => https://mail.google.com/")

async def youtube_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Batcave Surveillance => https://youtube.com/@adityabaisoya293?feature=shared")

async def linkedin_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Wayne Enterprises => https://www.linkedin.com/in/aditya-baisoya-632560257?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app")


async def instagram_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oracle's Social Feed => https://www.instagram.com/_adityabaisoya_?igsh=emF2eXVyOGdoaXd1")

# Unified mission command handler
async def mission_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if not args:
        await update.message.reply_text("Available actions: add, list, done, clear.\nExample: /mission add Patrol Gotham")
        return

    action = args[0].lower()

    if action == "add":
        task = " ".join(args[1:])
        if task:
            user_tasks[user_id].append(task)
            await update.message.reply_text(f"Mission added:\n- {task}")
        else:
            await update.message.reply_text("Usage: /mission add Interrogate Penguin at docks")

    elif action == "list":
        tasks = user_tasks.get(user_id, [])
        if tasks:
            formatted = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])
            await update.message.reply_text(f"Your missions:\n{formatted}")
        else:
            await update.message.reply_text("No active missions, master Bruce.")

    elif action == "done":
        if len(args) < 2 or not args[1].isdigit():
            await update.message.reply_text("Usage: /mission done [number]")
            return

        index = int(args[1]) - 1
        tasks = user_tasks.get(user_id, [])

        if 0 <= index < len(tasks):
            done_task = tasks.pop(index)
            await update.message.reply_text(f"Mission complete:\n- {done_task}")
        else:
            await update.message.reply_text("Invalid mission number.")

    elif action == "clear":
        user_tasks[user_id].clear()
        await update.message.reply_text("All missions cleared, master Bruce.")

    else:
        await update.message.reply_text("Unknown mission action. Use: add, list, done, or clear.")

# Unknown command
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"'{update.message.text}' is not recognized by the Batcomputer.")

# Unknown text
async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Message not understood: '{update.message.text}'. Try /help.")

# Main entry
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('batcave', youtube_url))
    app.add_handler(CommandHandler('wayne', linkedin_url))
    app.add_handler(CommandHandler('alfred', gmail_url))
    app.add_handler(CommandHandler('oracle', instagram_url))

    # Unified mission command
    app.add_handler(CommandHandler('mission', mission_handler))

    # Unknown message handlers
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), unknown_text))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Start polling
    app.run_polling()
