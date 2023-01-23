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

    def list(self, request, *args, **kwargs):
        print("LIST")
        return super().list(self, request, *args, **kwargs)

    def get_queryset(self):
        print("AHOIWHFOIAWHIO")
        queryset = super().get_queryset()
        category = queryset.filter(category_id=1)
        print(category)
        return random.choices(category, k=3)



