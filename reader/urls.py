from django.urls import path

from .views import (
    siradig_view,
    archivo_solo_view,
    procesa_view,
    )

urlpatterns = [
    path('', siradig_view, name='siradig'),
    path('procesa/', procesa_view, name='procesa-siradig'),
    path('solo/<slug>/', archivo_solo_view, name='archivoxml'),
]
