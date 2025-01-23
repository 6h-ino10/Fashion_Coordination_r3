from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from coordination_app.models import Item, Coordination
from django.urls import reverse
from unittest.mock import patch

class ItemListViewTest(TestCase):
    def setUp(self):
        self.test_image1 = SimpleUploadedFile(
            name = 'knit_gray.png',
            content = b'',
            content_type = 'image/png'
        )
        self.item1 = Item.objects.create(
            name = 'knit_gray',
            category = 'ニット',
            image = self.test_image1,
            season = 'Winter',
            memo = 'テスト用メモ'
        )

    def test_get_request(self):
        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item_list')
        self.assertIn('form', response.context)

    def test_item_register(self):
        self.assertEqual(self.item1.name, 'knit_gray')
        self.assertEqual(self.item1.category, 'ニット')
        self.assertEqual(self.item1.image, self.test_image1)
        self.assertEqual(self.item1.memo, 'テスト用メモ')

    def test_pagination(self):
        for i in range(6):
            Item.objects.create(
                name = f'item_{i}',
                category = 'カテゴリ',
                image = self.test_image1,
                memo = 'memo'
            )

        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['item_list']), 5)
        self.assertTrue(response.context['is_paginated'])

        response = self.client.get(reverse('item_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['item_list']), 2)

    @patch('users.views.get_weather_for_user')
    def test_weather_data(self, mock_get_weather):
        mock_get_weather.return_value = {'weather':'sunny', 'temperature': '20°C'}

        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)

        self.assertIn('weather_data', response.context)
        self.assertEqual(response.context['weather_data']['weather'], 'sunny')
        self.assertEqual(response.context['weather_data']['temperature'], '20°C')

class CoordinationListViewTest(TestCase):
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
            memo = 'テスト用メモ'
        )
        self.item2 = Item.objects.create(
            name = 'pants_black',
            category = 'パンツ',
            image = self.test_image2,
            season = 'Fall',
            memo = 'テスト用メモ'
        )
        self.coordination = Coordination.objects.create(
            category = 'カジュアル',
            season = 'Winter',
            coordination_image = self.coordination_image
        )

    def test_get_request(self):
        response = self.client.get(reverse('coordination_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coordination_list')
        self.assertIn('form', response.context)

    def test_coordination_register(self):
        self.assertEqual(self.coordination.category, 'カジュアル')
        self.assertEqual(self.coordination.season, 'Winter')
        self.assertEqual(self.coordination.coordination_image, self.coordination_image)

    def test_pagination(self):
        for i in range(6):
            Coordination.objects.create(
                category = 'カテゴリ',
                coordination_image = self.coordination_image,
                memo = 'memo'
            )

        response = self.client.get(reverse('coordination_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['coordination_list']), 5)
        self.assertTrue(response.context['is_paginated'])

        response = self.client.get(reverse('coordination_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['coordination_list']), 2)

    @patch('users.views.get_weather_for_user')
    def test_weather_data(self, mock_get_weather):
        mock_get_weather.return_value = {'weather':'sunny', 'temperature': '20°C'}

        response = self.client.get(reverse('coordination_list'))
        self.assertEqual(response.status_code, 200)

        self.assertIn('weather_data', response.context)
        self.assertEqual(response.context['weather_data']['weather'], 'sunny')
        self.assertEqual(response.context['weather_data']['temperature'], '20°C')

class CoordinationCreateViewTest(TestCase):
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

    def test_post_request(self):
        coordination_data = {
            'category':'カジュアル',
            'season':'Winter',
            'items':[self.item1.id, self.item2.id],
            'coordination_image':self.coordination_image
        }
        response = self.client.post(reverse('coordination_new'), data=coordination_data)
        self.assertEqual(response.status_code, 302)
        coordination = Coordination.objects.last()
        self.assertEqual(self.coordination.category, 'カジュアル')
        self.assertEqual(self.coordination.season, 'Winter')
        self.assertQuerySetEqual(self.coordination.items.order_by('id'), [repr(self.item1), repr(self.item2)])

    def test_error_handling(self):
            coordination_data = {
            'category':'カジュアル',
            'season':'',
            'items':[self.item1.id, self.item2.id],
            'coordination_image':self.coordination_image
            }
            response = self.client.post(reverse('coordination_new'), data=coordination_data)
            self.assertEqual(response.status_code, 200)
            self.assertFormError(response, 'form', 'season', 'このフィールドは必須です。')

class CoordinationUpdateViewTest(TestCase):
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
        self.coordination_image1 = SimpleUploadedFile(
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
            coordination_image = self.coordination_image1
        )
        self.coordination.items.set([self.item1, self.item2])

    def test_coordination_update(self):
        self.test_image3 = SimpleUploadedFile(
            name = 'skirt_green.png',
            content = b'',
            content_type = 'image/png'
        )
        self.item3 = Item.objects.create(
            name = 'skirt_green',
            category = 'スカート',
            image = self.test_image3,
            season = 'Fall',
            memo = ''
        )
        self.coordination_image2 = SimpleUploadedFile(
            name = 'coordination_winter_updated.png',
            content = b'',
            content_type = 'image/png'
        )

        coordination_data = {
            'category':'仕事',
            'season':'Fall',
            'items':[self.item1.id, self.item3.id],
            'coordination_image':self.coordination_image2
        }
        response = self.client.post(reverse('coordination_edit', kwargs={'pk':self.coordination.id}), data=coordination_data)

        self.coordination.refresh_from_db()

        self.assertRedirects(response, reverse('coordination_list'))
        self.assertEqual(self.coordination.category, '仕事')
        self.assertEqual(self.coordination.season, 'Fall')
        self.assertQuerySetEqual(self.coordination.items.all(), [self.item1, self.item3], transform=lambda x:x)
        self.assertEqual(self.coordination.coordination_image.name, 'coordination_winter_updated.png')



    
    
         
