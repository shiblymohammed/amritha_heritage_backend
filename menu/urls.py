from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailySpecialViewSet
from .views import make_reservation_api

router = DefaultRouter()
router.register(r'daily-specials', DailySpecialViewSet, basename='dailyspecial')

urlpatterns = [
    path('', include(router.urls)),
    path('make-reservation/', make_reservation_api, name='make_reservation_api'),
]