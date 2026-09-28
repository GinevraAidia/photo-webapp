from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, PostViewSet, ReactionViewSet

router = DefaultRouter()
router.register(r'event', EventViewSet, basename='event')
router.register(r'post', PostViewSet, basename='post')
router.register(r'reaction', ReactionViewSet, basename='reaction')

urlpatterns = [
    path('', include(router.urls)), 
]