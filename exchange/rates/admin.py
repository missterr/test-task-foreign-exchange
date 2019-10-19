from django.contrib import admin
from rates.models import Rate, Currency


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'date', 'rate', 'volume')


@admin.register(Currency)
class RateAdmin(admin.ModelAdmin):
    pass
