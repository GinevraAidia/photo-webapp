from django.urls import path
from . import views

urlpatterns=[
    path('event/', views.EventViewSet.as_view({'get': 'list'}), name='event-list'),
    path('post/', views.PostViewSet.as_view({'get':'list'}),name='post-list'),
    path('reaction/',views.ReactionViewSet.as_view({'get':'list'}),name='reaction-list'),
    path('eventShare/',views.EventShareViewSet.as_view({'get':'list'}),name='eventShare-list')
]