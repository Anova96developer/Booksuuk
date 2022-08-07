from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('',views.HelloAuthView.as_view(),name='hello_auth'),
    path('signup',views.UserCreateView.as_view(),name ='sign_up'),
    path('activate-account',views.AccountVerificationView.as_view(),name ='activate_account'),
    path('login',views.loginView.as_view(),name ='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]