from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/<int:pk>/cancel/', OrderViewSet.as_view({'put': 'cancel_order'}), name='cancel-order'),
    path('orders/<int:pk>/ship/', OrderViewSet.as_view({'put': 'ship_order'}), name='ship-order'),
    path('orders/<int:pk>/deliver/', OrderViewSet.as_view({'put': 'deliver_order'}), name='deliver-order'),
]