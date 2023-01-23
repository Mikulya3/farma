import random

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import request
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, ViewSet
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

User = get_user_model()

class CategoryAPIView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'price', 'description']
    ordering_fields = ['name', 'country', 'price', 'description']
    permission_classes = [IsAuthenticatedOrReadOnly]

class RecommendAPIView(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category_pk')
        Product.objects
        if category is not None:
            if queryset.get(request.product.id) is category.pk:
                result = random.choices(category.pk, k=3)
            return result



