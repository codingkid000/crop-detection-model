from django.urls import path
from .views import register_view, predict_view, history_view
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', register_view),
    path('login/', TokenObtainPairView.as_view()),
    path('predict/', predict_view),
    path('history/', history_view),
]