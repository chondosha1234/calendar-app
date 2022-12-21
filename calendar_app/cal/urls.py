from django.urls import path
from . import views

urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event_new, name='event_new'),
    path('event/create/', views.create_event, name='create_event'),
    path('event/details/<int:event_id>/', views.event_details, name ='event_details'),
    #path('event/edit/<int:event_id>/', views.EventEdit.as_view(), name='event_edit'),
    path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
]
