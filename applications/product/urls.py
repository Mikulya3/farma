from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.product.views import CategoryAPIView, ProductAPIView, RecommendAPIView, PaymentAPIView,OrderItemAPIView, OrderAPIView, OrderConfirmAPIView
from applications.product import views


router = DefaultRouter()
router.register('category', CategoryAPIView)
router.register('recommend', RecommendAPIView)
router.register('', ProductAPIView)
router.register('Payment', PaymentAPIView)
router.register('Orderitem', OrderItemAPIView)
router.register('Order', OrderAPIView)


urlpatterns = [
    path('', include(router.urls)),
    path('confirm/<uuid:code>/', OrderConfirmAPIView.as_view()),
    path('add-item-to-cart/<int:pk>', views.add_item_to_cart, name='add_item_to_cart'),
    path('cart-view/<int:pk>', views.cart_view, name='cart_view'),
    path('make-order/', views.make_order, name='make_order'),
]