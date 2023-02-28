from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('topics/', views.getCreateTopics),
    path('rooms/', views.getCreateRooms),
    path('rooms/<int:pk>/', views.getUpdateDeleteRoom),
    path('rooms/<int:pk>/participants/', views.getParticipants),
    path('rooms/<int:pk>/messages/', views.getMessages),
]