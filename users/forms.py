# users/forms.py

from django import forms
from .models import CustomUser, MEXICAN_STATES
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'second_last_name', 'phone_number', 
            'cedula', 'university', 'email', 'state'
        ]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Primer Apellido',
            'second_last_name': 'Segundo Apellido',
            'phone_number': 'Celular',
            'cedula': 'Cédula',
            'university': 'Universidad',
            'email': 'Correo Electrónico',
            'state': 'Estado'
        }
        widgets = {
            'state': forms.Select(choices=MEXICAN_STATES),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con ese correo electrónico.")
        return email

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if CustomUser.objects.filter(cedula=cedula).exists():
            raise forms.ValidationError("Ya existe un usuario con esa cédula.")
        return cedula


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Nombre de Usuario"),
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput
    )

    error_messages = {
        'invalid_login': _(
            "Por favor, introduce un nombre de usuario y una contraseña correctos. "
            "Ten en cuenta que ambos campos pueden ser sensibles a mayúsculas."
        ),
        'inactive': _("Esta cuenta está inactiva."),
    }
