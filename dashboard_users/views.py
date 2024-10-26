# dashboard_users/views.py

from collections import defaultdict
from datetime import datetime, timedelta
import random
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Examen, Pregunta, InscripcionExamen, UserExam
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CambiarContrasenaForm, InscripcionExamenForm
from django.core.paginator import Paginator
from django.db.models import Q


#------------------------------
#   DASHBOARD
#-------------------------------



class VistaDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard_users/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['usuario'] = user
        context['examenes_inscritos'] = InscripcionExamen.objects.filter(usuario=user)
        return context
    
#----------------------------------
#   CONTRASEÑA
#-----------------------------------

class CambiarContrasena(LoginRequiredMixin, View):
    form_class = CambiarContrasenaForm
    template_name = 'dashboard_users/cambiar_contrasena.html'

    def get(self, request):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contraseña cambiada con éxito.')
            return redirect('dashboard_users:dashboard')
        messages.error(request, 'Por favor corrige los errores a continuación.')
        return render(request, self.template_name, {'form': form})


#-----------------------------------------------
#      SALA DE ESPERA
#-----------------------------------------------
def sala_espera_examen(request, examen_id):
    # Obtener el examen por su ID
    examen = get_object_or_404(Examen, id=examen_id)
    
    # Obtener la fecha y hora del examen y asegurarse de que es timezone-aware
    examen_datetime = datetime.combine(examen.fecha, examen.hora)
    examen_datetime = timezone.make_aware(examen_datetime, timezone.get_current_timezone())

    # Obtener la hora actual y asegurarse de que es timezone-aware
    ahora = timezone.now()

    # Calcular el tiempo restante
    tiempo_restante = examen_datetime - ahora

    # Si ya es la hora del examen, redirigir al examen
    if tiempo_restante <= timedelta(0):
        return redirect('dashboard_users:generar_examen', examen_id=examen.id)

    # Si falta tiempo para el examen, mostrar la sala de espera
    context = {
        'examen': examen,
        'tiempo_restante': tiempo_restante
    }
    return render(request, 'dashboard_users/sala_espera.html', context)



#----------------------------------------
#   EXAMEN
#-----------------------------------------

class GenerarExamenView(View):
    template_name = 'dashboard_users/examen.html'
    http_method_names = ['get', 'post']

    def get(self, request, examen_id, page=1):
        # Obtener el UserExam del usuario
        user_exam = get_object_or_404(UserExam, examen_id=examen_id, usuario=request.user)

        # Verificar si el examen ya fue finalizado
        if user_exam.finalizado:
            messages.info(request, 'Este examen ya ha sido completado.')
            return redirect('dashboard_users:dashboard')

        # Obtener las preguntas del examen y la página actual
        preguntas = user_exam.preguntas.all().order_by('id')
        paginator = Paginator(preguntas, 20)
        pagina_actual = paginator.get_page(page)

        # Obtener las respuestas ya registradas (para mostrarlas si se regresa el usuario)
        respuestas_seleccionadas = user_exam.respuestas

        context = {
            'user_exam': user_exam,
            'pagina_actual': pagina_actual,
            'nombre_examen': user_exam.examen.nombre,
            'nombre_usuario': f"{request.user.first_name} {request.user.last_name}",
            'cedula': request.user.cedula,
            'correo': request.user.email,
            'modulo_actual': pagina_actual.object_list[0].modulo if pagina_actual.object_list else None,
            'respuestas_seleccionadas': respuestas_seleccionadas
        }

        return render(request, self.template_name, context)

    def post(self, request, examen_id, page=1):
        # Obtener el UserExam del usuario
        user_exam = get_object_or_404(UserExam, examen_id=examen_id, usuario=request.user)

        # Verificar si el examen ya fue finalizado
        if user_exam.finalizado:
            messages.error(request, 'Este examen ya ha sido completado.')
            return redirect('dashboard_users:dashboard')

        # Obtener la página actual del examen
        preguntas = user_exam.preguntas.all().order_by('id')
        pagina_actual = Paginator(preguntas, 20).get_page(page)

        # Imprimir los datos recibidos en el POST para depuración
        print("Datos del POST:", request.POST)

        # Guardar las respuestas enviadas
        respuestas_modificadas = False  # Bandera para verificar si hubo modificaciones

        for pregunta in pagina_actual:
            # Obtener la respuesta seleccionada del POST
            respuesta_usuario = request.POST.get(f'pregunta_{pregunta.id}', None)
            print(f"Pregunta ID: {pregunta.id}, Respuesta Seleccionada: {respuesta_usuario}")

            # Verificar si hay respuesta
            if respuesta_usuario:
                # Actualizar la respuesta en el diccionario de respuestas de UserExam
                if str(pregunta.id) not in user_exam.respuestas or user_exam.respuestas[str(pregunta.id)] != respuesta_usuario:
                    user_exam.respuestas[str(pregunta.id)] = respuesta_usuario
                    respuestas_modificadas = True
            else:
                # Guardar una indicación de que no se respondió
                if str(pregunta.id) not in user_exam.respuestas:
                    user_exam.respuestas[str(pregunta.id)] = None
                    respuestas_modificadas = True

        # Guardar los cambios solo si hubo modificaciones
        if respuestas_modificadas:
            print("Guardando respuestas modificadas")
            user_exam.save()

        # Verificar si el usuario presionó el botón de "anterior" o "siguiente"
        if 'anterior' in request.POST and pagina_actual.has_previous():
            return redirect('dashboard_users:generar_examen', examen_id=examen_id, page=pagina_actual.previous_page_number())
        elif 'siguiente' in request.POST and pagina_actual.has_next():
            return redirect('dashboard_users:generar_examen', examen_id=examen_id, page=pagina_actual.next_page_number())

        # Verificar si el usuario presionó el botón de "finalizar"
        if 'finalizar' in request.POST:
            user_exam.finalizado = True  # Cambia esto para establecer el examen como finalizado
            user_exam.calcular_nota()  # Asegúrate de que esto calcule y asigne la nota correctamente
            user_exam.save()  # Guarda los cambios en el modelo
            messages.success(request, 'Has completado el examen.')  # Mensaje de éxito
            return redirect('dashboard_users:dashboard')  # Redirigir al dashboard

        # Redirigir a la página actual del examen si algo sale mal
        return redirect('dashboard_users:generar_examen', examen_id=examen_id, page=page)



#---------------------------------
# INSCRIPCION
#---------------------------------

class InscripcionExamenView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard_users/inscripcion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasar el formulario con el usuario actual
        context['form'] = InscripcionExamenForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        # Pasar el usuario al formulario para manejar la lógica de validación
        form = InscripcionExamenForm(request.POST, user=request.user)
        if form.is_valid():
            examen = form.cleaned_data['examen']
            inscripcion, created = InscripcionExamen.objects.get_or_create(usuario=request.user, examen=examen)

            if created:
                # Crear una instancia de UserExam después de inscribirse
                user_exam = UserExam.objects.create(usuario=request.user, examen=examen)

                # Obtener las preguntas ya seleccionadas en el examen
                preguntas_examen = list(examen.preguntas.all())

                # Crear un diccionario para organizar las preguntas por módulo
                preguntas_por_modulo = {}

                for pregunta in preguntas_examen:
                    modulo = pregunta.modulo
                    if modulo not in preguntas_por_modulo:
                        preguntas_por_modulo[modulo] = []
                    preguntas_por_modulo[modulo].append(pregunta)

                # Crear una lista final para mantener las preguntas en orden
                preguntas_ordenadas = []

                # Organizar las preguntas dentro de cada módulo
                for modulo, preguntas_modulo in preguntas_por_modulo.items():
                    preguntas_modulo_barajadas = []

                    # Filtrar preguntas agrupadas y preguntas individuales
                    preguntas_agrupadas = {}
                    preguntas_individuales = []

                    for pregunta in preguntas_modulo:
                        if pregunta.identificador_de_grupo:
                            if pregunta.identificador_de_grupo not in preguntas_agrupadas:
                                preguntas_agrupadas[pregunta.identificador_de_grupo] = []
                            preguntas_agrupadas[pregunta.identificador_de_grupo].append(pregunta)
                        else:
                            preguntas_individuales.append(pregunta)

                    # Barajar las preguntas individuales
                    random.shuffle(preguntas_individuales)

                    # Añadir las preguntas agrupadas (sin barajar dentro del grupo, pero en orden aleatorio de grupos)
                    grupos_barajados = list(preguntas_agrupadas.values())
                    random.shuffle(grupos_barajados)

                    # Añadir las preguntas agrupadas y las individuales al módulo
                    for grupo in grupos_barajados:
                        preguntas_modulo_barajadas.extend(grupo)

                    preguntas_modulo_barajadas.extend(preguntas_individuales)

                    # Añadir las preguntas del módulo al listado general en el orden que corresponda
                    preguntas_ordenadas.extend(preguntas_modulo_barajadas)

                # Asignar las preguntas al UserExam respetando el orden por módulo
                user_exam.preguntas.set(preguntas_ordenadas)
                user_exam.save()

                messages.success(request, 'Te has inscrito exitosamente al examen.')
            else:
                messages.info(request, 'Ya estás inscrito en este examen.')

            # Redirigir al dashboard después de la inscripción
            return HttpResponseRedirect(reverse('dashboard_users:dashboard'))
        else:
            # Mostrar mensaje de error en caso de un formulario inválido
            messages.error(request, 'Ha ocurrido un error al inscribirte en el examen.')
            # Renderizar la misma página con el formulario inválido y sus errores
            return self.render_to_response(self.get_context_data(form=form))


