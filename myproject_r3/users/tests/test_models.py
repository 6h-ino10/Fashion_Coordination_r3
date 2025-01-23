from django.test import TestCase
from users.models import Region, UserProfile
from django.contrib.auth.models import User
import random

class RegionModelTest(TestCase):
    def test_all_prefectures_registered(self):
        prefectures = [
            '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県','茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県','新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県','滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県','鳥取県', '島根県', '岡山県', '広島県', '山口県','徳島県', '香川県', '愛媛県', '高知県','福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'
        ]

        for prefecture in prefectures:
            with self.subTest(prefecture=prefecture):
                self.assertTrue(Region.objects.filter(name=prefecture).exists())

class UserProfileModelTest(TestCase):
    def setUp(self):
        regions = Region.objects.all()
        self.random_region = random.choice(regions)
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=user, region=self.random_region)

    def test_user_profile_region(self):
        self.assertEqual(self.user_profile.region, self.random_region)
