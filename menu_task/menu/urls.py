from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:active_menu>/<int:active_item>', views.index, name='index')
]