from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserInfoView.as_view(), name='user-profile'),
    path('user/equipments/', views.UserEquipmentsView.as_view(), name='user-equipments'),
]
