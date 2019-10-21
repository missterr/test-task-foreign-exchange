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
        return Response({
            'latest_rate': instance.latest_rate,
            'average_volume': float(instance.get_volume_average(10))
        })

