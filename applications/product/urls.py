from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.product.views import CategoryAPIView, ProductAPIView, RecommendationAPIView

router = DefaultRouter()
router.register('category', CategoryAPIView)
router.register('', ProductAPIView)
router.register('recommend', RecommendationAPIView)

urlpatterns = [

    path('', include(router.urls)),

]