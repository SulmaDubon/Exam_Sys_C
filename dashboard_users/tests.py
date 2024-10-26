from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone as django_timezone  # Cambia el nombre aquí
from dashboard_users.models import Examen, Respuesta, UserExam, Pregunta, InscripcionExamen
from pytz import timezone as pytz_timezone  # Cambia el nombre aquí
from django.urls import reverse

CustomUser = get_user_model()

class InscripcionExamenModelTest(TestCase):
    
    def setUp(self):
        # Crear un usuario para la prueba
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        # Crear un examen para la prueba
        self.examen = Examen.objects.create(nombre='Examen de prueba', 
                                             fecha=django_timezone.now().date(),  # Usar el nuevo nombre
                                             hora=django_timezone.now().time())    # Usar el nuevo nombre

    def test_inscripcion_examen(self):
        inscripcion = InscripcionExamen.objects.create(usuario=self.user, examen=self.examen)
        self.assertEqual(inscripcion.usuario, self.user)
        self.assertEqual(inscripcion.examen, self.examen)


class ExamenModelTest(TestCase):
    def test_creacion_examen(self):
        examen = Examen.objects.create(nombre="Examen de prueba")
        self.assertEqual(examen.nombre, "Examen de prueba")
        self.assertEqual(examen.cantidad_preguntas, 260)  # Valor por defecto


def test_obtener_tiempo_limite(self):
    examen = Examen.objects.create(nombre="Examen con límite", tiempo_limite=210)
    self.assertEqual(examen.obtener_tiempo_limite(), "03:30")  # 210 minutos = 3h 30m


class PreguntaModelTest(TestCase):
    def test_creacion_pregunta(self):
        pregunta = Pregunta.objects.create(texto="¿Cuál es la capital de México?", tipo='A')
        self.assertEqual(pregunta.texto, "¿Cuál es la capital de México?")
        self.assertEqual(pregunta.tipo, 'A')


class UserExamModelTest(TestCase):
    
    def setUp(self):
        # Crear un usuario para la prueba
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        # Crear un examen para la prueba
        self.examen = Examen.objects.create(nombre='Examen de prueba', 
                                             fecha=django_timezone.now().date(),  # Usar el nuevo nombre
                                             hora=django_timezone.now().time())    # Usar el nuevo nombre

    def test_tiempo_restante(self):
        user_exam = UserExam.objects.create(usuario=self.user, examen=self.examen, inicio=django_timezone.now())
        self.assertEqual(user_exam.usuario, self.user)
        self.assertEqual(user_exam.examen, self.examen)


def test_calcular_nota(self):
    examen = Examen.objects.create(nombre="Examen de prueba")
    pregunta = Pregunta.objects.create(texto="¿Cuánto es 2 + 2?", tipo='A')
    respuesta_correcta = Respuesta.objects.create(pregunta=pregunta, texto="4", es_correcta=True)
    user_exam = UserExam.objects.create(usuario=self.user, examen=examen)
    user_exam.preguntas.add(pregunta)
    user_exam.respuestas = {str(pregunta.id): "4"}  # El usuario responde correctamente.
    user_exam.calcular_nota()
    self.assertEqual(user_exam.nota, 100.0)  # Nota perfecta.

def test_aprobacion_examen(self):
    examen = Examen.objects.create(nombre="Examen de prueba", aprobacion_minima=60.0)
    user_exam = UserExam.objects.create(usuario=self.user, examen=examen, nota=70.0)
    self.assertTrue(user_exam.aprobado())  # El examen debe estar aprobado.


class RespuestaModelTest(TestCase):
    def test_respuesta_correcta(self):
        pregunta = Pregunta.objects.create(texto="¿Capital de Francia?", tipo='A')
        respuesta = Respuesta.objects.create(pregunta=pregunta, texto="París", es_correcta=True)
        self.assertTrue(respuesta.es_correcta)
        self.assertEqual(respuesta.texto, "París")
        self.assertEqual(respuesta.pregunta, pregunta)

def test_sin_preguntas_suficientes(self):
    examen = Examen.objects.create(nombre="Examen sin preguntas")
    user_exam = UserExam.objects.create(usuario=self.user, examen=examen)
    user_exam.preguntas.clear()  # Vacía las preguntas
    with self.assertRaises(ValueError):
        user_exam.calcular_nota()

def test_flujo_examen_completo(self):
    examen = Examen.objects.create(nombre="Examen integral", tiempo_limite=210)
    pregunta = Pregunta.objects.create(texto="¿Capital de Italia?", tipo='A')
    respuesta_correcta = Respuesta.objects.create(pregunta=pregunta, texto="Roma", es_correcta=True)
    user_exam = UserExam.objects.create(usuario=self.user, examen=examen)
    user_exam.preguntas.add(pregunta)
    user_exam.respuestas = {str(pregunta.id): "Roma"}
    user_exam.calcular_nota()
    user_exam.examen_finalizado()
    
    self.assertTrue(user_exam.finalizado)
    self.assertEqual(user_exam.nota, 100.0)
    self.assertEqual(user_exam.estado, "Aprobado")


def test_zona_horaria(self):
    mexico_tz = pytz_timezone('America/Mexico_City')  # Cambia el nombre aquí
    examen = Examen.objects.create(nombre="Examen en Ciudad de México")
    self.assertEqual(examen.fecha.tzinfo.zone, mexico_tz.zone)   


class InscripcionExamenTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.examen = Examen.objects.create(nombre='Examen de Prueba', fecha='2024-12-01', hora='10:00', tipo='A')

    def test_inscripcion_examen_creacion(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('dashboard_users:inscripcion'), {'examen_id': self.examen.id})
        self.assertEqual(InscripcionExamen.objects.count(), 1)
        self.assertEqual(InscripcionExamen.objects.first().usuario, self.user)

    def test_no_doble_inscripcion(self):
        self.client.login(username='testuser', password='password')
        self.client.post(reverse('dashboard_users:inscripcion'), {'examen_id': self.examen.id})
        response = self.client.post(reverse('dashboard_users:inscripcion'), {'examen_id': self.examen.id})
        self.assertEqual(InscripcionExamen.objects.count(), 1)
        self.assertContains(response, 'Ya estás inscrito en este examen.')

    def test_inscripcion_examen_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('dashboard_users:inscripcion'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.examen.nombre)

    def test_inscripcion_examen_formulario(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('dashboard_users:inscripcion'), {'examen_id': self.examen.id})
        self.assertRedirects(response, reverse('dashboard_users:dashboard'))
        self.assertEqual(InscripcionExamen.objects.count(), 1)

    