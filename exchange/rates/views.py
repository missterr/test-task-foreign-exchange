from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authentication import BasicAuthentication

from rates.serializers import RateSerializer, CurrencySerializer
from rates.models import Rate, Currency


class RateView(ReadOnlyModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RateSerializer
    queryset = Rate.objects.all()
    pagination_class = LimitOffsetPagination


class CurrencyView(ReadOnlyModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    pagination_class = LimitOffsetPagination

    @action(methods=['get'], detail=True)
    def rate(self, request, *args, **kwargs):
        instance = self.get_object()
        latest_rate = instance.rate_set.order_by('date').last().rate
        avg_query = instance.rate_set.order_by('date')[:10].aggregate(Avg('volume'))
        # Could not find values which cannot be handled by float
        average_volume = float(avg_query.get('volume__avg'))
        return Response({'latest_rate': latest_rate,
                         'average_volume': average_volume})

