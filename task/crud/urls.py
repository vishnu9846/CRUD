from django.urls import path
from . import views

app_name="crud"

urlpatterns = [
    path('',views.account,name='account'),
    # path('', views.index, name='index'),
    path('reg/',views.reg, name='reg'),
    path('table/',views.table, name='table'),
    path('task/',views.task, name='task'),
    path('task/<int:pk>/update',views.update, name='update'),
    path('table/<int:pk>/delete/', views.delete, name='delete'),
    path('task/<int:pk>/complete/', views.task_complete, name='task_complete'),
    
  
    # Add other URLs for your application
]
