import logging
import os
from weather import get_weather
from currency import get_currency

logging.basicConfig(filename="app.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


if __name__ == "__main__":
    choice = input("Виберіть режим (weather/currency): ").strip().lower()

    if choice == "weather":
        city = input("Введіть місто: ")
        print(get_weather(city))
    elif choice == "currency":
        base = input("Базова валюта (наприклад USD): ") or "USD"
        symbols = input("Валюти для перевірки (наприклад EUR,UAH,PLN): ") or "EUR,UAH,PLN"
        print(get_currency(base, symbols))
    else:
        print("❌ Невідомий режим. Використовуйте 'weather' або 'currency'.")