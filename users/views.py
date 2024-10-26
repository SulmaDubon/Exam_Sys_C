from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, CustomAuthenticationForm
from .models import CustomUser
from django.views.generic.edit import FormView
import random
import string
import logging
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

#---------------------------
# Configurar el logger
#---------------------------

logger = logging.getLogger(__name__)

#--------------------------------
#  USERNAME & PASSWORD
#---------------------------------

def generate_username(first_name, last_name):
    base_username = f"{first_name.lower()}{last_name.lower()}"
    username = base_username
    counter = 1
    while CustomUser.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username

def generate_password(length=8):
    """Genera una contraseña aleatoria."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

#--------------------------------------
#  REGISTRO DE USUARIO Y ENVIO DE MAIL
#---------------------------------------

class UserRegistrationView(FormView):
    template_name = 'user/register.html'
    form_class = UserRegistrationForm
    success_url = '/'  # Cambia esto a la URL de tu página de inicio

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = generate_username(user.first_name, user.last_name)
        password = generate_password()
        user.set_password(password)
        try:
            user.save()
            send_mail(
                'Tus credenciales',
                f'Nombre de usuario: {user.username}\nContraseña: {password}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            messages.success(self.request, 'Usuario creado exitosamente. Revisa tu correo electrónico para las credenciales.')
            return redirect(self.get_success_url())
        except Exception as e:
            logger.error(f'Error al crear el usuario: {str(e)}')
            messages.error(self.request, 'Error al crear el usuario. Por favor, inténtelo de nuevo.')
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error con el formulario. Por favor, revisa los datos ingresados.')
        logger.warning(f"Formulario de registro no válido: {form.errors}")
        return self.render_to_response(self.get_context_data(form=form))


#-----------------------------------------------
#  LOGIN USUARIO
#-----------------------------------------------
@method_decorator(csrf_protect, name='dispatch')
class UserLoginView(ListView):
    template_name = 'user/login.html'  # Asegúrate de que esta línea esté presente

    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            logger.debug(f"Intentando autenticar al usuario: {username}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('dashboard_users:dashboard')
            else:
                logger.warning(f"Autenticación fallida para el usuario: {username}")
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        else:
            logger.warning(f"Formulario no válido: {form.errors}")
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        return render(request, self.template_name, {'form': form})

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')