from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.test, name='test'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutConfirmView.as_view(), name='logout_confirm'),
    path('logout/perform/', views.LogoutUserView.as_view(), name='logout'),
    path('signup/', views.SignupUserView.as_view(), name='signup'),
]