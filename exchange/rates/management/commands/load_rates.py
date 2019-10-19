import time
from datetime import datetime
from rates.utils import requests_retry_session
from rates.models import Rate, Currency
from django.core.management import BaseCommand

CURRENCIES = ('BTC', 'ETH', 'LTC', 'XRP', 'BAB')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for currency in Currency.objects.all():
            url = f'https://api-pub.bitfinex.com/v2/candles/trade:1D:t{currency.name}USD/hist?limit=10'

            response = requests_retry_session().get(url)
            response.raise_for_status()
            candles = response.json()

            rates = []

            for candle in candles:
                rates.append(
                    Rate(date=datetime.fromtimestamp(candle[0] / 1000.0),
                         currency=currency,
                         volume=candle[5],
                         rate=candle[2]
                         )
                )

            Rate.objects.bulk_create(rates)



