from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailySpecialViewSet
from .views import make_reservation_api, test_api, make_reservation_api_no_email

router = DefaultRouter()
router.register(r'daily-specials', DailySpecialViewSet, basename='dailyspecial')

urlpatterns = [
    path('', include(router.urls)),
    path('test/', test_api, name='test_api'),
    path('make-reservation/', make_reservation_api, name='make_reservation_api'),
    path('make-reservation-no-email/', make_reservation_api_no_email, name='make_reservation_api_no_email'),
]