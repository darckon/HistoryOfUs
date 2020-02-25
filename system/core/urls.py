from django.urls import include, path
from rest_framework import routers
from system.core import api as core_api

router = routers.DefaultRouter()

router.register('api/v1/users', core_api.UserViewSet),
router.register('api/v1/story_category', core_api.StoryCategoryViewSet),
router.register('api/v1/stories', core_api.StoryViewSet),
router.register('api/v1/questions', core_api.QuestionViewSet),
router.register('api/v1/movimientos', core_api.MovementViewSet),


urlpatterns = [

    # API
    path('', include(router.urls))

]
