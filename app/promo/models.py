from django.db import models
from django.utils.translation import gettext_lazy as l_

# Create your models here.
class Promocode(models.Model):
    
    image = models.ImageField(
        verbose_name=l_('Изображение'),
        upload_to="promocode/",
        blank=True,
        null=True,
    )
    code = models.CharField(
        verbose_name=l_('Промокод'),
        max_length=20,
        unique=True
    )
    discount = models.IntegerField(
        verbose_name=l_('Скидки (%)'),
        default=0
    )
    color = models.CharField(
        verbose_name=l_('Цвет'),
        max_length=10,
    )
    
    class Meta:
        verbose_name = l_('Промокод')
        verbose_name_plural = l_('Промокоды')
        
    def __str__(self):
        return self.code