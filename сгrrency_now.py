# import aiohttp
import requests
from datetime import datetime, timedelta


def currency():
    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        usd_rate = next(item['buy'] for item in data if item['ccy'] == 'USD')
        eur_rate = next(item['buy'] for item in data if item['ccy'] == 'EUR')

        return usd_rate, eur_rate
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None


def withdrawal_in_10_days():
    start_date = datetime.now()
    end_date = start_date + timedelta(days=10)

    for i in range(10):
        formatted_date = (start_date + timedelta(days=i)).strftime('%d.%m.%Y')
        url = f"https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid={formatted_date}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            usd_rate = next(item['purchaseRateNB'] for item in data['exchangeRate'] if item['currency'] == 'USD')
            eur_rate = next(item['purchaseRateNB'] for item in data['exchangeRate'] if item['currency'] == 'EUR')

            print(f"Date: {formatted_date}, USD rate: {usd_rate}, EUR rate: {eur_rate}")
        else:
            print(f"Failed to retrieve data for {formatted_date}. Status code: {response.status_code}")


if __name__ == "__main__":
    rates = currency()

    if rates:
        usd_rate, eur_rate = rates
        print(f"USD rate: {usd_rate}")
        print(f"EUR rate: {eur_rate}")

    withdrawal_in_10_days()
