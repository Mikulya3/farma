from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.product.views import CategoryAPIView, ProductAPIView, RecommendAPIView

router = DefaultRouter()
router.register('category', CategoryAPIView)
router.register('recommend', RecommendAPIView)
router.register('', ProductAPIView)



urlpatterns = [
    path('', include(router.urls)),
]