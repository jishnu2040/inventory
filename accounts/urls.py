from django.urls import path
from .views import RegisterUserView, LoginUserView  # Ensure these imports are correct

urlpatterns = [
    
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'), 
]
