# dashboard_users/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(str(key))  # Asegúrate de convertir la clave en string

