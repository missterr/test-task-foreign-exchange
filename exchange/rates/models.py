from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.name


class Rate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateField()
    rate = models.FloatField(default=1.0)
    volume = models.DecimalField(decimal_places=8, max_digits=24)

    def __str__(self):
        return f'{self.currency.name} - {self.date}'

