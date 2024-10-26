from django.urls import path
from .views import (
    AdminLoginView,
    VistaAdminPanel,
    ListaUsuarios, CrearUsuario, EditarUsuario, EliminarUsuario,
    ListaExamenes, CrearExamen, EditarExamen, EliminarExamen,
    UsuariosInscritosView,
    ListaPreguntas, CrearPreguntaView, PreguntaDeleteView,
    AccionesExamenesView,
    TipoExamenListView, CrearTipoExamenView, EditarTipoExamenView, TipoExamenDeleteView,
    get_modulos,
    SubirPreguntasView, ActualizarPreguntasView,
    ResultadosAdministrador,
    generar_informe_examen,
    certificado,
)

app_name = 'admin_panel'

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin_login'),
    path('', VistaAdminPanel.as_view(), name='admin_panel'),  # Ruta raíz para el panel de administración
    path('usuarios/', ListaUsuarios.as_view(), name='lista_usuarios'),
    path('usuarios/crear/', CrearUsuario.as_view(), name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', EditarUsuario.as_view(), name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', EliminarUsuario.as_view(), name='eliminar_usuario'),
    
    # Exámenes
    path('examenes/', ListaExamenes.as_view(), name='lista_examenes'),
    path('examenes/crear/', CrearExamen.as_view(), name='crear_examen'),
    path('examenes/editar/<int:pk>/', EditarExamen.as_view(), name='editar_examen'),
    path('examenes/eliminar/<int:pk>/', EliminarExamen.as_view(), name='eliminar_examen'),
    path('examenes/usuarios-inscritos/<int:pk>/', UsuariosInscritosView.as_view(), name='usuarios_inscritos'),
    path('examenes/acciones/', AccionesExamenesView.as_view(), name='acciones_examenes'),

    # Preguntas
    path('preguntas/', ListaPreguntas.as_view(), name='lista_preguntas'),
    path('preguntas/crear/', CrearPreguntaView.as_view(), name='pregunta_create'),
    path('preguntas/eliminar/<int:pk>/', PreguntaDeleteView.as_view(), name='pregunta_delete'),
    path('preguntas/subir/', SubirPreguntasView.as_view(), name='subir_preguntas'),
    path('preguntas/actualizar/', ActualizarPreguntasView.as_view(), name='actualizar_preguntas'),

    # Tipo de Examenes
    path('tipo_examen/', TipoExamenListView.as_view(), name='lista_tipo_examen'),  
    path('tipo_examen/crear/', CrearTipoExamenView.as_view(), name='crear_tipo_examen'),
    path('tipo_examen/editar/<int:pk>/', EditarTipoExamenView.as_view(), name='editar_tipo_examen'),
    path('tipo_examen/eliminar/<int:pk>/', TipoExamenDeleteView.as_view(), name='eliminar_tipo_examen'),

    # Ruta para obtener módulos por tipo de examen
    path('get-modulos/<int:tipo_examen_id>/', get_modulos, name='get_modulos'),

    # Resultados administrador
    path('examenes/resultados/<int:examen_id>/', ResultadosAdministrador.as_view(), name='resultados_administrador'),  
    path('generar-informe-examen/', generar_informe_examen, name='generar_informe_examen'),  # Ruta para generar informe de examen
    path('certificado/<int:user_exam_id>/', certificado, name='certificado'),  # Ruta para el certificado
]
