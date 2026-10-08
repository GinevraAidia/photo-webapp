from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, PostReactionViewSet, PostViewSet, ReactionViewSet, UserViewSet

router = DefaultRouter()
router.register(r'event', EventViewSet, basename='event')
router.register(r'post', PostViewSet, basename='post')
router.register(r'reaction', PostReactionViewSet, basename='postReaction')
router.register(r'users',UserViewSet,basename='user')
router.register(r'typeReaction',ReactionViewSet,basename='reaction')

urlpatterns = [
    path('', include(router.urls))
]