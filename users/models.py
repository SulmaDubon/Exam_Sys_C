# users/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

MEXICAN_STATES = [
    ('AG', 'Aguascalientes'), ('BC', 'Baja California'), ('BS', 'Baja California Sur'),
    ('CM', 'Campeche'), ('CS', 'Chiapas'), ('CH', 'Chihuahua'), ('CO', 'Coahuila'),
    ('CL', 'Colima'), ('DF', 'Ciudad de México'), ('DG', 'Durango'), ('GT', 'Guanajuato'),
    ('GR', 'Guerrero'), ('HG', 'Hidalgo'), ('JA', 'Jalisco'), ('EM', 'Estado de México'),
    ('MI', 'Michoacán'), ('MO', 'Morelos'), ('NA', 'Nayarit'), ('NL', 'Nuevo León'),
    ('OA', 'Oaxaca'), ('PU', 'Puebla'), ('QT', 'Querétaro'), ('QR', 'Quintana Roo'),
    ('SL', 'San Luis Potosí'), ('SI', 'Sinaloa'), ('SO', 'Sonora'), ('TB', 'Tabasco'),
    ('TM', 'Tamaulipas'), ('TL', 'Tlaxcala'), ('VE', 'Veracruz'), ('YU', 'Yucatán'),
    ('ZA', 'Zacatecas')
]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    second_last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    cedula = models.CharField(max_length=20, unique=True)
    university = models.CharField(max_length=100)
    registration_date = models.DateField(auto_now_add=True)
    state = models.CharField(max_length=2, choices=MEXICAN_STATES)

    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='customuser_customuser_set')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_customuser_set',
        help_text=_('Specific permissions for this user.'),
    )

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

    def __str__(self):
        return f"{self.username} ({self.email})"


