import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY_CURR")  # ключ збережи у .env

def get_currency(base: str = "USD", symbols: str = "EUR,UAH,PLN") -> str:
    """
    Отримати курси валют через Currency Exchange API.
    Args:
        base (str): базова валюта
        symbols (str): список валют через кому
    Returns:
        str: форматований рядок з курсами
    """
    url = f"https://api.currencyapi.com/v3/latest?base_currency={base}&currencies={symbols}"
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers).json()

    if "data" not in response:
        return f"❌ Помилка: {response}"

    rates = response["data"]
    message = f"Курси валют (база {base}):\n"
    for symbol, info in rates.items():
        message += f"1 {base} = {info['value']:.2f} {symbol}\n"

    return message.strip()
