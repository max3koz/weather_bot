import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, \
	ContextTypes

from config import TELEGRAM_BOT_TOKEN
from weather import get_weather
from currency import get_currency

user_state = {}

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

print("TELEGRAM_BOT_TOKEN:", TELEGRAM_BOT_TOKEN)  # 👈 це з’явиться у логах

if not TELEGRAM_BOT_TOKEN:
    print("❌ Змінна TELEGRAM_BOT_TOKEN не задана. Контейнер завершено.")
    exit(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	"""
	Handler for the /start command.
	Args:
		- update (telegram.Update): Object with data about the user's message.
		- context (telegram.ext.ContextTypes.DEFAULT_TYPE): Execution context.
	Returns: None: Sends a welcome message with a short instruction.
	"""
	await update.message.reply_text("Привіт! Я бот для погоди. "
	                                "Використай /help щоб дізнатися більше.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
	"""
	Handler for the /help command.
	Args:
		- update (telegram.Update): Object with data about the user's message.
		- context (telegram.ext.ContextTypes.DEFAULT_TYPE): Execution context.
	Returns: None: Sends a list of available bot commands.
	"""
	await update.message.reply_text(
		"/start – привітання\n"
		"/help – список команд\n"
		"/weather – отримати погоду з подальшим вибором міста\n"
		"/weather <назва міста> – отримати погоду у вказаному місті")


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
	"""
	Handler for the /weather command.
	Args:
		- update (telegram.Update): Object with data about the user's message.
		- context (telegram.ext.ContextTypes.DEFAULT_TYPE): Execution context.
		  Used to get arguments after the command (/weather Kyiv).
	Returns: None: Sends the weather forecast for the specified city
	or an instruction, if no city was passed.
	"""
	user_id = update.message.from_user.id
	
	if context.args:
		city = " ".join(context.args)
		result = get_weather(city)
		await update.message.reply_text(result)
	else:
		user_state[user_id] = "waiting_city"
		await update.message.reply_text(
			"Будь ласка, вкажіть місто. Приклад: /weather Київ")
		

async def currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for the /currency command.
    Args:
        - update (telegram.Update): Object with data about the user's message.
        - context (telegram.ext.ContextTypes.DEFAULT_TYPE): Execution context.
    Returns: None: Sends exchange rates for selected currencies.
    """
    base = "USD"
    symbols = "EUR,UAH,PLN"

    if context.args:
        # Якщо користувач передав аргументи: /currency EUR,UAH
        symbols = ",".join(context.args)

    result = get_currency(base, symbols)
    await update.message.reply_text(result)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
	"""
	Handler for processing text messages that are not commands.
	Args:
		- update (telegram.Update): An object with data about the user's message.
		- context (telegram.ext.ContextTypes.DEFAULT_TYPE): Execution context.
	Returns: None: If the user is in the 'waiting_city' state, interprets
	the message as the name of the city, gets the forecast and sends it
	to the user.
	"""
	user_id = update.message.from_user.id
	if user_state.get(user_id) == "waiting_city":
		city = update.message.text
		result = get_weather(city)
		await update.message.reply_text(result)
		user_state[user_id] = None


def run_bot():
	"""
	Starts the Telegram bot.
		- Initializes the application with a token.
		- Registers handlers for commands (/start, /help, /weather).
		- Registers a handler for regular text messages.
		- Starts a polling loop.
	Returns: None: Prints a startup message to the console and starts the bot.
	"""
	try:
		app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
	
		app.add_handler(CommandHandler("start", start))
		app.add_handler(CommandHandler("help", help_command))
		app.add_handler(CommandHandler("weather", weather))
		app.add_handler(CommandHandler("currency", currency))
		app.add_handler(
			MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
		print("Бот запущено...")
		app.run_polling()
	except Exception as e:
		print("❌ Помилка при запуску бота:", e)
		exit(1)
