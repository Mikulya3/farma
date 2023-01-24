from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from applications.product.models import Payment, Order, OrderItem
from applications.product.serializers import PaymentSerializer, OrderSerializer, OrderItemSerializer
import random
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import request, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, ViewSet
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

User = get_user_model()

class PaymentAPIView(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

class CategoryAPIView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'price', 'description']
    ordering_fields = ['title', 'country', 'price', 'description']
    permission_classes = [IsAuthenticatedOrReadOnly]

class RecommendAPIView(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        category = queryset.filter(category_id=1)
        return random.choices(category, k=3)

class OrderAPIView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset
class OrderConfirmAPIView(APIView):
    def get(self, request, code):
        order = get_object_or_404(Order, activation_code=code)
        if not order.is_confirm:
            order.is_confirm = True
            order.status = 'STATUS_WAITING_FOR_PAYMENT '
            order.save(update_fields=['is_confirm', 'status'])
            return Response({'message': 'Вы подтвердили заказ!'}, status=status.HTTP_200_OK)
        return Response({'message': 'Вы уже подтвердили заказ!'}, status=status.HTTP_400_BAD_REQUEST)

class OrderItemAPIView(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


@login_required(login_url=reverse_lazy('login'))
def add_item_to_cart(request, pk):
    if request.method == 'POST':
        quantity = OrderItemSerializer(request.POST)
        if OrderItemSerializer.is_valid():
            quantity = OrderItemSerializer.cleaned_data['quantity']
            if quantity:
                cart = Order.get_cart(request.user)
                product = get_object_or_404(Product, pk=pk)
                cart.orderitem_set.create(product=product,
                                          quantity=quantity,
                                          price=product.price)
                cart.save()
                return redirect('payment')
        else:
            pass
    return redirect('product')
@login_required(login_url=reverse_lazy('login'))
def cart_view(request):
    cart = Order.objects.get(request.user)
    items = cart.orderitem_set.all()
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, context)

@method_decorator(login_required, name='dispatch')
class CartDeleteItem(DeleteView):
    model = OrderItem
    success_url = reverse_lazy('cart_view')
    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(order__user=self.request.user)
        return qs
@login_required(login_url=reverse_lazy('login'))
def make_order(request):
    cart = Order.objects.get(request.user)
    cart.make_order()
    return redirect('product')
