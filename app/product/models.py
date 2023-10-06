from django.db import models
from django.utils.translation import gettext_lazy as l_

# Create your models here.
class Category(models.Model):
    
    position = models.SmallIntegerField(
        verbose_name=l_('Позиция'),
    )
    name = models.CharField(
        verbose_name=l_('Название'),
        max_length=128,
    )
    image = models.FileField(
        verbose_name=l_('Изображение'),
        blank=False,
        null=False,
        max_length=256,
        upload_to='categories/'
    )
    color = models.CharField(
        verbose_name=l_('Цвет'),
        max_length=16
    )
    
    class Meta:
        verbose_name = l_('Категория')
        verbose_name_plural = l_('Категории')
        
    def __str__(self):
        return self.name
        

class Product(models.Model):
    
    category = models.ForeignKey(
        Category,
        verbose_name=l_('Категория'),
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    name = models.CharField(
        verbose_name=l_('Название'),
        max_length=64,
    )
    description = models.CharField(
        verbose_name=l_('Описание'),
        max_length=128,
    )
    price = models.FloatField(
        verbose_name=l_('Цена'),
        default=0,
    )
    image = models.ImageField(
        verbose_name=l_('Изображение'),
        upload_to='products/',
        blank=True,
        null=True,
        default=None
    )
    
    class Meta:
        verbose_name = l_('Товар')
        verbose_name_plural = l_('Товары')
        
    def __str__(self):
        return self.name
