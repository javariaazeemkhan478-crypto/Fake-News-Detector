from django.contrib import admin
from django.urls import path
from detector.views import PredictView, AnalyticsView, LoginView, LogoutView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/register/', RegisterView.as_view()),
    path('api/predict/', PredictView.as_view()),
    path('api/analytics/', AnalyticsView.as_view()),
]