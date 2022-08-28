from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView


from django.urls import path,include

from rest_framework import routers
from . import views

app_name = "account"
router  = routers.DefaultRouter()

router.register('',viewset=views.AuthViewSets)

urlpatterns = [
   path ('',include(router.urls)),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
   path('token/verify', TokenVerifyView.as_view(), name='token_verify'),

]




# urlpatterns = [
#     path('users',views.AllUsers.as_view(),name='hello_auth'),
#     path('signup',views.UserCreateView.as_view(),name ='sign_up'),
#     path('activate-account',views.AccountVerificationView.as_view(),name ='activate_account'),
#     path('login',views.loginView.as_view(),name ='login'),
#     path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
#     path('token/verify', TokenVerifyView.as_view(), name='token_verify'),


# ]