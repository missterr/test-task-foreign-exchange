from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rates.views import RateView, CurrencyView

router = routers.SimpleRouter()
router.register(r'rates', RateView)
router.register(r'currencies', CurrencyView)

urlpatterns = [
    path('admin/', admin.site.urls),
] + router.urls
