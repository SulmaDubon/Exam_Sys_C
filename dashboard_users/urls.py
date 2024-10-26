from django.urls import path
from .views import (
    VistaDashboard,
    CambiarContrasena,
    InscripcionExamenView,
    GenerarExamenView,
    sala_espera_examen,
)

app_name = 'dashboard_users'

urlpatterns = [
    path('', VistaDashboard.as_view(), name='dashboard'),
    path('cambiar_contrasena/', CambiarContrasena.as_view(), name='cambiar_contrasena'),
    path('inscripcion/', InscripcionExamenView.as_view(), name='inscripcion'),
    path('examen/<int:examen_id>/', GenerarExamenView.as_view(), name='generar_examen'),
    path('examen/<int:examen_id>/<int:page>/', GenerarExamenView.as_view(), name='generar_examen_paginado'),  # Nueva ruta para paginación
    path('sala_espera/<int:examen_id>/', sala_espera_examen, name='sala_espera_examen'),
]


