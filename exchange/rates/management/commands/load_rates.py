from datetime import datetime
from django.core.management import BaseCommand
from rates.utils import requests_retry_session
from rates.models import Rate, Currency


class Command(BaseCommand):
    def handle(self, *args, **options):
        for currency in Currency.objects.all():
            currency.rate_set.all().delete()
            url = f'https://api-pub.bitfinex.com/v2/candles/trade:1D:t{currency.name}USD/hist?limit=10'

            nonce = int(datetime.timestamp(datetime.now()) * 1000000)
            response = requests_retry_session(headers={'bfx-nonce': nonce},
                                              retries=5, backoff_factor=0.3).get(url)
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



