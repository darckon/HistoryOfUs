from django.contrib import admin
from django.urls import include, path
from core import views as index_views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from core import api as core_api

router = routers.DefaultRouter()
router.register('users', core_api.UserViewSet),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_views.index, name='index'),

    #RestFramework
    path('api-auth/', include('rest_framework.urls')),

    #API
    path('', include(router.urls)),

    #RestFramework - JWT
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
]
