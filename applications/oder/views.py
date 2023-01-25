from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from requests import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from applications.oder.models import  Order
from applications.oder.serializers import  OrderSerializer



User = get_user_model()

class OrderAPIView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OrderConfirmAPIView(APIView):

    def get(self, request, code):
        order = get_object_or_404(Order, code)
        if not order.is_confirm:
            order.is_confirm = True
            order.status = 'STATUS_WAITING_FOR_PAYMENT '
            order.save(update_fields=['is_confirm', 'status'])
            return Response({'message': 'Вы подтвердили заказ!'}, status=status.HTTP_200_OK)
        return Response({'message': 'Вы уже подтвердили заказ!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=['GET'])
def cart_view(request):
    cart = Order.objects.get(request.user)
    items = cart.order_set.all()
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, context)

class CartDeleteItemDetail(APIView):
    def delete(self, request,pk):
        cart = Order.objects.get(request.user)
        items = cart.order_set.all()
        items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET'])
def make_order(request):
    cart = Order.objects.get(request.user)
    cart.make_order()
    return redirect('product')
