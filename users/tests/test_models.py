# users/tests/test_models.py

from django.test import TestCase
from users.models import CustomUser

class CustomUserModelTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='testuser',
            email='test@example.com',
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            cedula='ABC12345',
            university='Some University',
            state='JA'  # Jalisco, por ejemplo
        )

    def test_user_creation(self):
        self.assertEqual(CustomUser.objects.count(), 1)
        saved_user = CustomUser.objects.get(username='testuser')
        self.assertEqual(saved_user.email, 'test@example.com')
        self.assertEqual(saved_user.get_full_name(), 'John Doe')

    def test_user_state_choices(self):
        self.assertIn(self.user.state, dict(CustomUser.MEXICAN_STATES).keys())

    # Agrega más pruebas según sea necesario
