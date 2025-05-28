from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.test),
    path('signin/', views.LoginUserView.as_view(), name='login'),
]