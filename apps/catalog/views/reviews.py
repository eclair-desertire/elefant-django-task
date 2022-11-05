from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from apps.catalog import serializers
from apps.catalog.models import Review
from rest_framework.viewsets import ModelViewSet

class BookReview(ModelViewSet):
    permission_classes=[IsAuthenticated,]
    serializer_class=serializers.ReviewSerializer
    queryset=Review.objects.all()

    @extend_schema(
        request=serializer_class,
        responses={200: serializer_class},
        methods=['POST'],
        tags=['Reviews']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

