from django.urls import path
from . import views
from search.views import SearchView
from .views import ValidateOTP, ResendOtpView, UserLoginAPIView, Testemail, PasswordResetAPIView, validate_password_reset_otp
# from search import SearchView



urlpatterns = [
	path('create/', views.user_create, name='user_create'),
	path('list/', views.user_list_viewset, name='user_list'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
	path('<int:pk>/', views.user_detail_viewset, name='user_detail_viewset'),
	path('', views.user_detail, name='user_detail'),
    path('testing/', Testemail.as_view(), name='testing'),
	path('<int:pk>/update/', views.user_update_viewset, name='user_update'),
	path('change-password/', views.change_password, name='change_password'),
    # path('login-with-otp/', LoginWithOTP.as_view(), name='login-with-otp'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('validate-reset-password/', validate_password_reset_otp, name='validate-reset-password'),
    path('validate-otp/', ValidateOTP.as_view(), name='validate-otp'),
    path('resend-otp/', ResendOtpView.as_view(), name='resend-otp'),
]