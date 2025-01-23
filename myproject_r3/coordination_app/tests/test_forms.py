from django.test import TestCase
from coordination_app.models import Item
from coordination_app.forms import CoordinationForm
from django.core.files.uploadedfile import SimpleUploadedFile

class CoordinationFormTest(TestCase):
    def setUp(self):
        self.test_image1 = SimpleUploadedFile(
            name = 'knit_gray.png',
            content = b'',
            content_type = 'image/png'
        )
        self.test_image2 = SimpleUploadedFile(
            name = 'pants_black.png',
            content = b'',
            content_type = 'image/png'
        )
        self.item1 = Item.objects.create(
            name = 'knit_gray',
            category = 'ニット',
            image = self.test_image1,
            season = 'Winter',
            memo = ''
        )
        self.item2 = Item.objects.create(
            name = 'pants_black',
            category = 'パンツ',
            image = self.test_image2,
            season = 'Fall',
            memo = ''
        )
        self.test_image = SimpleUploadedFile(
            name = 'test_image.png',
            content = b'',
            content_type = 'image/png'
        )
 
    def test_coordination_register(self):
        form_data = {
            'category':'カジュアル',
            'season':'Winter',
            'items':[self.item1.id, self.item2.id],
            'coordination_image':self.test_image
        }
        form = CoordinationForm(data=form_data, files={'coordination_image':self.test_image})
        self.assertTrue(form.is_valid())
        coordination = form.save()
        self.assertEqual(coordination.category, 'カジュアル')
        self.assertEqual(coordination.season, 'Winter')
        self.assertIn(self.item1, coordination.items.all())
        self.assertIn(self.item2, coordination.items.all())
