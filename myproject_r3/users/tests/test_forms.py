from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfile, Region
from users.forms import UserChangeForm, RegionForm
import random

class UserChangeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user, defaults={'region':None})

    def test_user_change_form(self):
        form_data = {
            'username':'new_testuser',
            'email':'new_test@example.com',
            'password':'new_testpassword'
        }
        form = UserChangeForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

        updated_user = form.save()
        self.assertEqual(updated_user.username, 'new_testuser')
        self.assertEqual(updated_user.email, 'new_test@example.com')
        self.assertEqual(updated_user.check_password, 'new_testpassword')

class RegionFormTest(TestCase):
    def setUp(self):
        self.region1 = Region.objects.create(name='東京都')
        self.region2 = Region.objects.create(name='大阪府')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user, defaults={'region':self.region1})

    def test_region_setup(self):
        new_region = random.choice(Region.objects.all())
        form_data = {'region':new_region.id}
        form = RegionForm(data=form_data, instance=self.user_profile)

        self.assertTrue(form.is_valid())
        updated_profile = form.save()
        self.assertEqual(updated_profile.region, new_region)
