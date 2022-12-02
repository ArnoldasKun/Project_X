from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blacksmiths', views.blacksmiths, name='blacksmiths'),
    path('blacksmith/<int:blacksmith_id', views.blacksmith, name='blacksmith'),
    path('armors/', views.ArmorListView.as_view(), name='armors')
]