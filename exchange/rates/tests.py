import json
import factory
import factory.fuzzy
from datetime import datetime
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from rates.models import Currency, Rate


PASSWORD = '123Qwertyu'


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'Test User {}'.format(n))
    first_name = factory.fuzzy.FuzzyText(length=30)
    last_name = factory.fuzzy.FuzzyText(length=30)
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())
    password = factory.PostGenerationMethodCall('set_password', PASSWORD)

    class Meta:
        model = User


class CurrencyFactory(factory.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText(length=3)

    class Meta:
        model = Currency


class RateFactory(factory.DjangoModelFactory):
    currency = factory.SubFactory(CurrencyFactory)
    date = factory.fuzzy.BaseFuzzyDateTime(start_dt=datetime(2019, 1, 1), end_dt=datetime.now())
    rate = factory.fuzzy.FuzzyFloat(low=0.0)
    volume = factory.fuzzy.FuzzyDecimal(low=0.0, high=99999999.99999999, precision=8)

    class Meta:
        model = Rate


class ExchangeAPITestCase(APITestCase):
    def setUp(self) -> None:
        super(ExchangeAPITestCase, self).setUp()
        self.user = UserFactory(email='test@3test.com', username='Main user for tests')
        self.currencies = CurrencyFactory.create_batch(5)
        [RateFactory.create_batch(10, currency=cur) for cur in self.currencies]

    def test_retrieve_currency_list(self):
        url = reverse('currency-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_retrieve_volume_avg(self):
        currency = self.currencies[0]
        url = reverse('currency-detail', args=(currency.id,))
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('currency-rate', args=(currency.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(json.dumps(response.data),
                             json.dumps({'latest_rate': currency.latest_rate,
                                         'average_volume': float(currency.get_volume_average(10))}))


