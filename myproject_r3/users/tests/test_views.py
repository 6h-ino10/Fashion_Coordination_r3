from django.test import TestCase
from users.views import get_weather_for_user
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Region, UserProfile
from unittest.mock import patch


class ProfileEditViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_get_request(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        self.assertIn('form', response.context)

    def test_post_request_user_update(self):
        form_data = {
            'username':'new_username',
            'email':'new_test@example.com',
            'password':''
        }
        response = self.client.post(reverse('edit_profile'), data=form_data)
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_username')
        self.assertEqual(self.user.email, 'new_test@example.com')

    def test_post_request_password_update(self):
        password_data = {
            'old_password':'testpassword',
            'new_password1':'new_testpassword',
            'new_password2':'new_testpassword'
        }
        response = self.client.post(reverse('edit_profile'), data=password_data)
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_testpassword'))

    def test_error_handling(self):
        invalid_data = {
            'username':'',
            'email':'invalid_email_format'
        }
        response = self.client.post(reverse('edit_profile'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertContains(response, 'このフィールドは必須です。')

class RegionRegisterViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')


    def test_get_request(self):
        response = self.client.get(reverse('region'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'region_register.html')
        self.assertIn('form', response.context)

    def test_post_request_region_register(self):
        data = {
            'region':'東京都'
        }
        response = self.client.post(reverse('region'), data=data)
        self.assertRedirects(response, reverse('item_list'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.userprofile.region.name, '東京都')

    def test_error_handling(self):
        invalid_data = {
            'region':''
        }
        response = self.client.post(reverse('region'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'region_register.html')
        self.assertContains(response, 'このフィールドは必須です。')

class GetWeatherForUserViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.region = Region.objects.create(name='東京都')
        self.user_profile = UserProfile.objects.create(user=self.user, region=self.region)
        self.client.login(username='testuser', password='testpassword')

    @patch('users.views.get_weather_data')
    def test_get_weather_for_user_with_region(self, mock_get_weather_data):
        mock_get_weather_data.return_value = {'weather':[{'description':'晴れ'}], 'main':{'temp':25}}

        weather_data = get_weather_for_user(self.user)
        self.assertIsNotNone(weather_data)
        self.assertIn('weather', weather_data)
        self.assertEqual(weather_data['weather'][0]['description'], '晴れ')

    def test_get_weather_for_user_without_region(self):
        self.user_profile.region = None
        self.user_profile.save()

        weather_data = get_weather_for_user(self.user)
        self.assertIsNone(weather_data)

    @patch('users.views.get_weather_data')
    def test_weather_display_in_item_list(self, mock_get_weather_data):
        mock_get_weather_data.return_value = {'weather':[{'description':'晴れ'}], 'main':{'temp':25}}

        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '晴れ')
        self.assertContains(response, '25')

    @patch('users.views.get_weather_data')
    def test_weather_display_in_coordination_list(self, mock_get_weather_data):
        mock_get_weather_data.return_value = {'weather':[{'descroption':'曇り'}], 'main':{'temp':20}}

        response = self.client.get(reverse('coordination_list'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '曇り')
        self.assertContains(response, '20')

        



