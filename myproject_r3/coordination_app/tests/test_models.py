from django.test import TestCase
from coordination_app.models import Item, Coordination
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class ItemModelTest(TestCase):
    def setUp(self):
        self.test_image = SimpleUploadedFile(
            name = 'knit_gray.png',
            content = b'',
            content_type = 'image/png'
        )
        self.item = Item.objects.create(
            name = 'knit_gray',
            category = 'ニット',
            image = self.test_image,
            season = 'Winter',
            memo = 'テスト用のメモ'
        )

    def test_item_creation(self):
        self.assertEqual(self.item.name, 'knit_gray')
        self.assertEqual(self.item.category, 'ニット')
        self.assertEqual(self.item.image.name, 'knit_gray.png')
        self.assertEqual(self.item.season, 'Winter')
        self.assertEqual(self.item.memo, 'テスト用のメモ')

    def test_item_string_representation(self):
        self.assertEqual(str(self.item), 'knit_gray')

    def test_get_absolute_url(self):
        self.assertEqual(self.item.get_absolute_url(), reverse('item_list'))

class CoordinationModelTest(TestCase):
    def setUp(self,):
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
        self.coordination_image = SimpleUploadedFile(
            name = 'coordination_winter.png',
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
        self.coordination = Coordination.objects.create(
            category = 'カジュアル',
            season = 'Winter',
            coordination_image = self.coordination_image
        )
        self.coordination.items.set([self.item1, self.item2])

    def test_items_association(self):
        items = self.coordination.items.all()
        self.assertIn(self.item1, items)
        self.assertIn(self.item2, items)
        self.assertEqual(items.count(), 2)

    def test_coordination_creation(self):
        self.assertEqual(self.coordination.category, 'カジュアル')
        self.assertEqual(self.coordination.coordination_image.name, 'coordination_winter.png')
        self.assertEqual(self.coordination.season, 'Winter')

    def test_get_absolute_url(self):
        self.assertEqual(self.coordination.get_absolute_url(), reverse('coordination_list'))

