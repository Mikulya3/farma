from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.oder.views import OrderAPIView, OrderConfirmAPIView, cart_view, CartDeleteItemDetail, make_order

router = DefaultRouter()
router.register('', OrderAPIView)

urlpatterns = [
    path('confirm/<uuid:code>/', OrderConfirmAPIView.as_view()),
    path('cart_view/', cart_view),
    path('deleteitems/', CartDeleteItemDetail.as_view()),
    path('make-order/', make_order),
    path('', include(router.urls)),
]