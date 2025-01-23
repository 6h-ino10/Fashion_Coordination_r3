from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

    
class Item(models.Model):
    CATEGORY_CHOICE = [
        ('カットソー', 'カットソー'),
        ('ブラウス', 'ブラウス'),
        ('ニット', 'ニット'),
        ('パンツ', 'パンツ'),
        ('スカート', 'スカート'),
        ('ワンピース', 'ワンピース'),
        ('シューズ', 'シューズ'),
    ]
    SEASON_CHOICES = [
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Fall', 'Fall'),
        ('Winter', 'Winter'),
    ]

    name = models.CharField(max_length=200,default="")
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICE,
        default='カットソー',
    )
    image = models.ImageField(blank=True,default='noImage.png')
    season = models.CharField(
        max_length=10,
        choices=SEASON_CHOICES,
        default='Spring',
    )
    memo = models.CharField(max_length=200,default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('item_list')
    

class Coordination(models.Model):
    CATEGORY_CHOICE = [
        ('カジュアル', 'カジュアル'),
        ('仕事', '仕事'),
        ('マニッシュ', 'マニッシュ'),
        ('フェミニン', 'フェミニン'),
    ]
    SEASON_CHOICES = [
        ('Spring','Spring'),
        ('Summer','Summer'),
        ('Fall','Fall'),
        ('Winter','Winter'),
    ]
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICE,
        default='カジュアル',
    )

    season = models.CharField(
        max_length=10,
        choices=SEASON_CHOICES,
        default='Spring',
    )
    items = models.ManyToManyField(Item,related_name='coordinations')
    coordination_image = models.ImageField(upload_to='coordination_images/',blank=True,default='noImage.png')
    memo = models.CharField(max_length=200,default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.season:
            return f'Coordination for {self.season}'
        elif self.memo:
            return self.memo
        else:
            return ""

    def get_absolute_url(self):
        return reverse('coordination_list')

