from django.urls import include, path
from rest_framework import routers
from system.core import api as core_api

router = routers.DefaultRouter()

router.register('api/v1/users', core_api.UserViewSet),
router.register('api/v1/categoria_historias', core_api.CategoriaHistoriaViewSet),
router.register('api/v1/historias', core_api.HistoriaViewSet),
router.register('api/v1/preguntas', core_api.PreguntasViewSet),
router.register('api/v1/movimientos', core_api.MovimientosViewSet),


urlpatterns = [

    # API
    path('', include(router.urls))

]
